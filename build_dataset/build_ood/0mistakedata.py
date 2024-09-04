import json
import shutil
import os

def mistake():
    # JSON文件路径
    json_file_path = 'misclassified_images_cf.json'
    # 错误图片存放文件夹路径
    error_images_folder = 'error_images_folder'

    # 确保错误图片文件夹存在
    os.makedirs(error_images_folder, exist_ok=True)

    # 读取JSON文件
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # 遍历数据并复制错误图片
    for entry in data:
        image_path = entry['image_name']
        prediction = entry['prediction']
        answer = entry['answer']

        # 判断是否为错误图片
        if prediction != answer:
            # 获取文件名
            image_name = os.path.basename(image_path)
            # 构建目标文件路径
            target_path = os.path.join(error_images_folder, image_name)
            # 复制文件
            shutil.copy(image_path, target_path)

    print("错误图片复制完成")


import json
import re
from collections import Counter

# JSON文件路径
json_file_path = 'misclassified_images_cf.json'

# 读取JSON文件
with open(json_file_path, 'r') as file:
    data = json.load(file)

# 创建一个计数器来统计物品的出现次数
item_counter = Counter()

# 正则表达式匹配物品名称
pattern = re.compile(r'There are \d+ (.+) in the image')

# 遍历数据并提取物品名称
for entry in data:
    prediction = entry['prediction']

    # 查找并提取物品名称
    match = pattern.search(prediction)
    if match:
        item_name = match.group(1)
        item_counter[item_name] += 1

# 输出物品名称及其出现次数
for item, count in item_counter.items():
    print(f"{item}: {count}")
