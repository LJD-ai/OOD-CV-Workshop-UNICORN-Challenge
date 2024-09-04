import json
import shutil
import os

# 定义 JSON 文件路径
json_file_path = "sketchy_error_images_25000_cf.json"  # 将此路径替换为你的JSON文件路径

# 读取 JSON 数据
with open(json_file_path, 'r') as file:
    data = json.load(file)

# 定义源文件夹和目标文件夹路径
source_folder = ""  # 根据你的实际路径进行调整
base_destination_folder = "./wrong_sk_cf_25000"  # 将此路径替换为你的目标文件夹路径
# '/sketches_png/png/book/1999.png'
# 创建目标文件夹（如果不存在）
os.makedirs(base_destination_folder, exist_ok=True)

# 遍历 JSON 数据并复制文件
for item in data:
    image_name = item["image_name"]
    label = image_name.split("/")[-2]
    destination_folder = os.path.join(base_destination_folder, f"{label}")
    # 创建目标文件夹（如果不存在）
    os.makedirs(destination_folder, exist_ok=True)
    # source_path = os.path.join(source_folder, os.path.basename(image_name))
    # source_path ='.'+ image_name
    source_path = image_name
    destination_path = os.path.join(destination_folder, os.path.basename(image_name))

    # 复制文件
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        print(f"已成功复制: {source_path} 到 {destination_path}")
    else:
        print(f"文件不存在: {source_path}")
# import os
#
# def list_classes(dataset_path):
#     # 获取数据集路径下的所有文件夹，即类别名称
#     classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
#     classes.sort()  # 按照字母顺序排序，方便查看
#     return classes
#
# # 指定数据集路径
# dataset_path = './wrong_sk_cf'
# classes = list_classes(dataset_path)
#
# # 打印所有类别
# print("Found classes:")
# for cls in classes:
#     print(cls)
