import json
import random

# 读取之前生成的 JSON 文件
with open('train_top_categories_per_image15000.json', 'r') as f:
    top_categories_per_image = json.load(f)

# 计算每张图片中的总目标数量
image_target_counts = [
    (index, sum(categories.values()))
    for index, image in enumerate(top_categories_per_image)
    for categories in [image['top_categories']]
]

# 按照目标数量进行排序（从少到多）
image_target_counts.sort(key=lambda x: x[1])

# 从目标较少的图片中选择500张
selected_indices = [index for index, _ in image_target_counts[:1000]]

# 向选中的150张图片添加 "unicorn: 0" 标签
for index in selected_indices:
    top_categories_per_image[index]['top_categories']['unicorn'] = 0

# 保存修改后的 JSON 文件
with open('train_top_categories_per_image_with_unicorn15000.json', 'w') as f:
    json.dump(top_categories_per_image, f, indent=4)

print("JSON文件已生成：train_top_categories_per_image_with_unicorn15000.json")
