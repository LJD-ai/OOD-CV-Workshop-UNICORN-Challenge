# OOD-CV-Workshop-UNICORN-Challenge
OOD-CV Workshop UNICORN Challenge: Team LJDljd's Approach
<!-- <p align="center">
  <img src="unicorn.png" width="80">
</p> -->

## Installation
For Qwen-VL-Chat, please refer to their specific envirnments for installation.
- Qwen-VL-Chat: https://huggingface.co/Qwen/Qwen-VL-Chat
Place the downloaded model in the model folder.

## Datasets
The datasets [here](https://huggingface.co/datasets/PahaII/vllm_safety_evaluation), containing both OOD and redteaming attack datasets. The ood dataset should looks like this:

```
.
├── ./safety_evaluation_benchmark_datasets//                    
    └── ood # Contains the test data for OOD scenarios
        ├── sketchy-vqa
            ├── sketchy-vqa.json
            ├── sketchy-challenging.json
        └── oodcv-vqa
            ├── oodcv-vqa.json
            └── oodcv-counterfactual.json
```

### Out-of-Distribution Scenario
For $\texttt{OODCV-VQA}$ and its counterfactual version, please download images from [OODCV](https://drive.google.com/file/d/1jq43Q0cenISIq7acW0LS-Lqghgy8exsj/view?usp=share_link), and put all images in `ood/oodcv-vqa`.

For $\texttt{Sketchy-VQA}$ and its challenging version, please first download images from [here](https://cybertron.cg.tu-berlin.de/eitz/projects/classifysketch/sketches_png.zip), put the zip file into `ood/sketchy-vqa/skechydata/`, then unzip it.
## Testing
Before you start, make sure you have modified the `CACHE_DIR` (where you store all your model weights) and `DATA_DIR` (where you store the benchmark data) in `baselines/config.json` according to your local envirnment.

```bash
python model_testing_zoo.py --model_name Qwen-VL-Chat
```
Choose `--model_name` from ["LlamaAdapterV2", "MiniGPT4", "MiniGPT4v2", "LLaVA", "mPLUGOwl", "mPLUGOwl2", "PandaGPT", "InstructBLIP2", "Flamingo", "LLaVAv1.5", "LLaVAv1.5-13B", "LLaVA_llama2-13B", "MiniGPT4_llama2", "Qwen-VL-Chat", "MiniGPT4_13B", "InstructBLIP2-FlanT5-xl", "InstructBLIP2-FlanT5-xxl",  "InstructBLIP2-13B", "CogVLM", "Fuyu", "InternLM"].

## Inference
### $\texttt{OODCV-VQA}$ and its Counterfactual Variant

For $\texttt{OODCV-VQA}$:
```bash
cd ./safety_evaluations/ood_scenarios
python evaluation.py --model_name Qwen-VL-Chat --eval_oodcv
```

For the counterfactual version:

```bash
cd ./safety_evaluations/ood_scenarios
python evaluation.py --model_name Qwen-VL-Chat --eval_oodcv_cf
```

### $\texttt{Sketchy-VQA}$ and its Challenging Variant

For $\texttt{Sketchy-VQA}$:
```bash
cd ./safety_evaluations/ood_scenarios
python evaluation.py --model_name Qwen-VL-Chat --eval_sketch
```

For the challenging version:

```bash
cd ./safety_evaluations/ood_scenarios
python evaluation.py --model_name Qwen-VL-Chat --eval_sketch_challenging
```

Run getresult-ood.py and getresult-sketchy.py to generate the results for submission.
## train

```bash
python3 /Qwen-VL/finetune.py \
    --model_name_or_path /model/Qwen-VL-Chat \
    --data_path /fintune_data/data.json \
    --bf16 True \
    --fix_vit True \
    --output_dir output_qwen \
    --num_train_epochs 5 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 1000 \
    --save_total_limit 10 \
    --learning_rate 1e-5 \
    --weight_decay 0.1 \
    --adam_beta2 0.95 \
    --warmup_ratio 0.01 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --report_to "none" \
    --model_max_length 600 \
    --lazy_preprocess True \
    --gradient_checkpointing true \
    --use_lora
```
model_name_or_path is the path where the model is stored, and data_path is the path to the data used for fine-tuning.
The data used for fine-tuning is stored in fintune_data.output_dir is the path for model output.

The data used for OOD-VQA training comes from COCO2017, specifically train2017. The data for Sketchy-VQA training comes from QuickDraw and some additional data from the internet, which need to be downloaded by yourself. You also need to modify the image paths in the data.json file accordingly.

The other code related to the creation of the dataset used for fine-tuning is saved in the build_dataset folder.
