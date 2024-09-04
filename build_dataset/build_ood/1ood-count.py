import json
import pandas as pd
import random
from collections import defaultdict

# 加载 JSON 文件
with open('./COCO2017/annotations_trainval2017/annotations/instances_train2017.json', 'r') as f:
    coco_data = json.load(f)

# 提取图像信息和注释信息
images = coco_data['images']
annotations = coco_data['annotations']
categories = coco_data['categories']

# 创建类别映射字典 (category_id -> category_name)
category_map = {category['id']: category['name'] for category in categories}

# 初始化一个字典来存储每个图像中每个类别的计数
image_category_count = defaultdict(lambda: defaultdict(int))

# 统计每张图片中每个类别的数量
for annotation in annotations:
    image_id = annotation['image_id']
    category_id = annotation['category_id']
    image_category_count[image_id][category_map[category_id]] += 1

# 随机选择 10,000 张图片
random_images = random.sample(images, min(15000, len(images)))

# 将结果转换为列表，每个元素代表一行数据
data = []
for image in random_images:
    image_id = image['id']
    image_filename = image['file_name']
    row = {'image_id': image_id, 'file_name': image_filename}
    row.update(image_category_count[image_id])
    data.append(row)

# 转换为DataFrame
df = pd.DataFrame(data)

# 用0填充缺失值
df = df.fillna(0)

# 将所有计数列转换为整数
for category in category_map.values():
    if category in df.columns:
        df[category] = df[category].astype(int)

# 保存为CSV文件
df.to_csv('coco_train2017_category_counts_sampled15000.csv', index=False)

print("CSV文件已生成：coco_train2017_category_counts_sampled15000.csv")
