export PATH=/cpfs01/shared/public/shusheng.yss/anaconda3/envs/ofa2_py38_cu118_pth201_kosmos/bin:$PATH

checkpoint=../

# caption
for ds in "flickr" "nocaps"
do
    python -m torch.distributed.launch --use-env \
        --nproc_per_node ${NPROC_PER_NODE:-8} --nnodes 1 \
        evaluate_caption.py \
        --checkpoint $checkpoint \
        --dataset $ds \
        --batch-size 8 \
        --num-workers 2 \
        --few-shot 0
done

# vqa
for ds in "okvqa_val" "textvqa_val" "vizwiz_val"
do
    python -m torch.distributed.launch --use-env \
        --nproc_per_node ${NPROC_PER_NODE:-8} --nnodes 1 \
        evaluate_vqa.py \
        --checkpoint $checkpoint \
        --dataset $ds \
        --batch-size 8 \
        --num-workers 2 \
        --few-shot 0
done

# fewshot vqa
for fs in 1 2 4
do
    for ds in  "okvqa_val" "vizwiz_val"
    do
        python -m torch.distributed.launch --use-env \
            --nproc_per_node ${NPROC_PER_NODE:-8} --nnodes 1 \
            evaluate_vqa.py \
            --checkpoint $checkpoint \
            --dataset $ds \
            --batch-size 8 \
            --num-workers 2 \
            --few-shot $fs
    done
done

# vizwiz testdev
python -m torch.distributed.launch --use-env \
    --nproc_per_node ${NPROC_PER_NODE:-8} --nnodes 1 \
    evaluate_vizwiz_testdev.py \
    --checkpoint $checkpoint \
    --dataset $ds \
    --batch-size 8 \
    --num-workers 2 \
    --few-shot $fs

# multiple choice
for ds in "scienceqa_test_img"
do
    python -m torch.distributed.launch --use-env \
        --nproc_per_node ${NPROC_PER_NODE:-8} --nnodes 1 \
        evaluate_multiple_choice.py \
        --checkpoint $checkpoint \
        --dataset $ds \
        --batch-size 8 \
        --num-workers 2
done

# grounding
for ds in "refcoco_val" "refcoco_testA" "refcoco_testB" "refcoco+_val" "refcoco+_testA" "refcoco+_testB" "refcocog_val" "refcocog_test"
do
    python -m torch.distributed.launch --use-env \
        --nproc_per_node ${NPROC_PER_NODE:-8} --nnodes 1 \
        evaluate_grounding.py \
        --checkpoint $checkpoint \
        --dataset $ds \
        --batch-size 8 \
        --num-workers 2
done
