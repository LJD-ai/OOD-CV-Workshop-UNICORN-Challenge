import os
import cv2

# 定义原始数据集路径和保存灰度图的目标路径
# input_dir = 'bing_simplified_drawings'  # 请根据你的数据集路径修改
# output_dir = 'huidu_sk'
input_dir = 'mydraw2'  # 请根据你的数据集路径修改
output_dir = 'huidu_my2'
# 创建目标文件夹
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image_counter = 1  # 用于图像编号

# 遍历数据集中的所有类和图片
for class_name in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_name)
    if os.path.isdir(class_path):
        # 为每个类别创建一个对应的子文件夹
        output_class_path = os.path.join(output_dir, class_name)
        if not os.path.exists(output_class_path):
            os.makedirs(output_class_path)

        # 遍历类别中的所有图片
        for image_name in os.listdir(class_path):
            image_path = os.path.join(class_path, image_name)
            if image_path.endswith(('jpg', 'jpeg', 'png', 'bmp')):
                # 读取图片并转换为灰度图
                image = cv2.imread(image_path)
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # 生成新的图像文件名，使用编号
                new_image_name = f"{image_counter:05d}.jpg"  # 例如：00001.jpg
                output_image_path = os.path.join(output_class_path, new_image_name)

                # 保存灰度图至目标路径
                cv2.imwrite(output_image_path, gray_image)

                # 增加编号
                image_counter += 1

print("图片已成功转换为灰度图、编号，并保存至零一文件夹。")
