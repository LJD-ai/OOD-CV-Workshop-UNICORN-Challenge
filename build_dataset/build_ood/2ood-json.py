import pandas as pd
import json

# 读取CSV文件
df = pd.read_csv('coco_train2017_category_counts_sampled15000.csv')

# 初始化一个空列表来存储结果
top_categories_per_image = []

# 遍历每一行（每张图片）
for _, row in df.iterrows():
    image_id = row['image_id']
    file_name = row['file_name']

    # 去除'file_name' 和 'image_id'列，剩下的是类别列
    categories = row.drop(labels=['image_id', 'file_name'])

    # 过滤掉类别数目为0的项
    categories = categories[categories > 0]

    # 按数量排序，并提取前三名
    top_categories = categories.sort_values(ascending=False).head(3)

    # 构建字典存储每张图片的前三类别信息
    top_categories_dict = {
        'image_id': int(image_id),
        'file_name': file_name,
        'top_categories': top_categories.to_dict()
    }

    top_categories_per_image.append(top_categories_dict)

# 将结果保存为JSON文件
with open('train_top_categories_per_image15000.json', 'w') as f:
    json.dump(top_categories_per_image, f, indent=4)

print("JSON文件已生成：train_top_categories_per_image15000.json")
