import argparse
import itertools
import json
import os
import random
import time
from functools import partial

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from vqa import VQA
from vqa_eval import VQAEval

ds_collections = {
    'vqav2_val': {
        'train': 'data/vqav2/vqav2_train.jsonl',
        'test': 'data/vqav2/vqav2_val.jsonl',
        'question': 'data/vqav2/v2_OpenEnded_mscoco_val2014_questions.json',
        'annotation': 'data/vqav2/v2_mscoco_val2014_annotations.json',
        'metric': 'vqa_score',
    },
    'okvqa_val': {
        'train': 'data/okvqa/okvqa_train.jsonl',
        'test': 'data/okvqa/okvqa_val.jsonl',
        'question': 'data/okvqa/OpenEnded_mscoco_val2014_questions.json',
        'annotation': 'data/okvqa/mscoco_val2014_annotations.json',
        'metric': 'vqa_score',
    },
    'textvqa_val': {
        'train': 'data/textvqa/textvqa_train.jsonl',
        'test': 'data/textvqa/textvqa_val.jsonl',
        'question': 'data/textvqa/textvqa_val_questions.json',
        'annotation': 'data/textvqa/textvqa_val_annotations.json',
        'metric': 'vqa_score',
    },
    'vizwiz_val': {
        'train': 'data/vizwiz/vizwiz_train.jsonl',
        'test': 'data/vizwiz/vizwiz_val.jsonl',
        'question': 'data/vizwiz/vizwiz_val_questions.json',
        'annotation': 'data/vizwiz/vizwiz_val_annotations.json',
        'metric': 'vqa_score',
    }
}


def collate_fn(batches, tokenizer):

    questions = [_['question'] for _ in batches]
    question_ids = [_['question_id'] for _ in batches]

    input_ids = tokenizer(questions, return_tensors='pt', padding='longest')

    return question_ids, input_ids.input_ids, input_ids.attention_mask


class VQADataset(torch.utils.data.Dataset):

    def __init__(self, train, test, prompt, few_shot):
        self.test = open(test).readlines()
        self.prompt = prompt

        self.few_shot = few_shot
        if few_shot > 0:
            self.train = open(train).readlines()

    def __len__(self):
        return len(self.test)

    def __getitem__(self, idx):
        data = json.loads(self.test[idx].strip())
        image, question, question_id = data['image'], data['question'], data[
            'question_id']

        few_shot_prompt = ''
        if self.few_shot > 0:
            few_shot_samples = random.sample(self.train, self.few_shot)
            for sample in few_shot_samples:
                sample = json.loads(sample.strip())
                few_shot_prompt += self.prompt.format(
                    sample['image'],
                    sample['question']) + f" {sample['answer']}"

        return {
            'question': few_shot_prompt + self.prompt.format(image, question),
            'question_id': question_id,
        }


class InferenceSampler(torch.utils.data.sampler.Sampler):

    def __init__(self, size):
        self._size = int(size)
        assert size > 0
        self._rank = torch.distributed.get_rank()
        self._world_size = torch.distributed.get_world_size()
        self._local_indices = self._get_local_indices(size, self._world_size,
                                                      self._rank)

    @staticmethod
    def _get_local_indices(total_size, world_size, rank):
        shard_size = total_size // world_size
        left = total_size % world_size
        shard_sizes = [shard_size + int(r < left) for r in range(world_size)]

        begin = sum(shard_sizes[:rank])
        end = min(sum(shard_sizes[:rank + 1]), total_size)
        return range(begin, end)

    def __iter__(self):
        yield from self._local_indices

    def __len__(self):
        return len(self._local_indices)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, default='')
    parser.add_argument('--dataset', type=str, default='')
    parser.add_argument('--batch-size', type=int, default=1)
    parser.add_argument('--num-workers', type=int, default=1)
    parser.add_argument('--few-shot', type=int, default=0)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()

    torch.distributed.init_process_group(
        backend='nccl',
        world_size=int(os.getenv('WORLD_SIZE', '1')),
        rank=int(os.getenv('RANK', '0')),
    )

    torch.cuda.set_device(torch.distributed.get_rank())

    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint, device_map='cuda', trust_remote_code=True).eval()

    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint,
                                              trust_remote_code=True)
    tokenizer.padding_side = 'left'
    tokenizer.pad_token_id = tokenizer.eod_id

    prompt = '<img>{}</img>{} Answer:'

    random.seed(args.seed)
    dataset = VQADataset(
        train=ds_collections[args.dataset]['train'],
        test=ds_collections[args.dataset]['test'],
        prompt=prompt,
        few_shot=args.few_shot,
    )

    dataloader = torch.utils.data.DataLoader(
        dataset=dataset,
        sampler=InferenceSampler(len(dataset)),
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=True,
        drop_last=False,
        collate_fn=partial(collate_fn, tokenizer=tokenizer),
    )

    outputs = []
    for _, (question_ids, input_ids,
            attention_mask) in tqdm(enumerate(dataloader)):
        pred = model.generate(
            input_ids=input_ids.cuda(),
            attention_mask=attention_mask.cuda(),
            do_sample=False,
            num_beams=1,
            max_new_tokens=10,
            min_new_tokens=1,
            length_penalty=1,
            num_return_sequences=1,
            output_hidden_states=True,
            use_cache=True,
            pad_token_id=tokenizer.eod_id,
            eos_token_id=tokenizer.eod_id,
        )
        answers = [
            tokenizer.decode(_[input_ids.size(1):].cpu(),
                             skip_special_tokens=True).strip() for _ in pred
        ]

        for question_id, answer in zip(question_ids, answers):
            outputs.append({'question_id': int(question_id), 'answer': answer})

    torch.distributed.barrier()

    world_size = torch.distributed.get_world_size()
    merged_outputs = [None for _ in range(world_size)]
    torch.distributed.all_gather_object(merged_outputs, outputs)

    merged_outputs = [_ for _ in itertools.chain.from_iterable(merged_outputs)]

    if torch.distributed.get_rank() == 0:
        time_prefix = time.strftime('%y%m%d%H%M%S', time.localtime())
        results_file = f'{args.dataset}_{time_prefix}_fs{args.few_shot}_s{args.seed}.json'
        json.dump(merged_outputs, open(results_file, 'w'),
                  ensure_ascii=False)  # save to results

        vqa = VQA(ds_collections[args.dataset]['annotation'],
                  ds_collections[args.dataset]['question'])
        results = vqa.loadRes(
            resFile=results_file,
            quesFile=ds_collections[args.dataset]['question'])
        vqa_scorer = VQAEval(vqa, results, n=2)
        vqa_scorer.evaluate()

        print(vqa_scorer.accuracy)

    torch.distributed.barrier()
