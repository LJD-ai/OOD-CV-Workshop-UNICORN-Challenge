import json

def combine_json_files(file1_path, file2_path, output_path):
    # 读取第一个JSON文件
    with open(file1_path, 'r') as file1:
        data1 = json.load(file1)

    # 读取第二个JSON文件
    with open(file2_path, 'r') as file2:
        data2 = json.load(file2)

    # 合并两个文件的数据
    combined_data = data1 + data2

    # 重新计算ID
    for i, item in enumerate(combined_data):
        item['id'] = f"identity_{i}"

    # 将合并后的数据写入新的JSON文件
    with open(output_path, 'w') as output_file:
        json.dump(combined_data, output_file, indent=2)

# 示例路径
file1_path = 'ood_vqa.json'  # 替换为第一个JSON文件的路径
file2_path = 'generated_conversations15000_vqa2.json'  # 替换为第二个JSON文件的路径
output_path = 'ood_vqa_all.json'  # 替换为合并后的JSON文件保存路径

# 运行函数
combine_json_files(file1_path, file2_path, output_path)
