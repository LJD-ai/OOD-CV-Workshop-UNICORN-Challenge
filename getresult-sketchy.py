import json

# 输入文件路径
input_file = 'safety_evaluations/test_results/sketchyvqa_generated/sketchyvqa_challenging_results_Qwen-VL-Chat_final.json'
# 输出文件路径
output_file = 'Sketchy-Challenging_final.json'

# 从文件中读取 JSON 数据
with open(input_file, 'r') as f:
    data = json.load(f)

# 删除每个对象中的 `label` 和 `answer` 字段
for item in data:
    if 'label' in item:
        del item['label']
    if 'answer' in item:
        del item['answer']

    # 修改 `image_path` 字段
    if 'image_path' in item:
        # 替换路径的一部分
        new_path = item['image_path'].replace('/home/pod/VLLM/data/dataset/safety_evaluation_benchmark_datasets/ood/sketchy-vqa/sketchespng', 'sketch')
        # 替换斜杠为下划线
        new_path = new_path.replace('/', '_')
        item['image_path'] = new_path

# 将修改后的数据保存到新的 JSON 文件
with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Modified JSON data has been saved to {output_file}")