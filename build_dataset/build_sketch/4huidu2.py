import os
import cv2
import numpy as np

# 定义灰度图像文件夹路径和保存处理后图像的目标路径
# input_dir = 'huidu_sk'  # 使用已生成的灰度图数据集
# output_dir = 'huidu_sk3'  # 保存处理后的图像
input_dir = 'huidu_my2'  # 使用已生成的灰度图数据集
output_dir = 'huidu_my23'  # 保存处理后的图像
# 创建目标文件夹
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 设置灰度阈值，小于这个值的部分设置为纯黑色，大于等于这个值的部分设置为纯白色
threshold = 50  # 你可以根据需要调整这个值

# 遍历数据集中所有类别和图片
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
                # 读取灰度图像
                gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                if gray_image is None:
                    print(f"错误: 无法读取图像 {image_path}. 跳过此图像.")
                    continue  # 如果无法读取图像，跳过这个文件

                # 将低于阈值的像素设置为纯黑色（0），高于等于阈值的像素设置为纯白色（255）
                binary_image = np.where(gray_image < threshold, 0, 255).astype(np.uint8)

                # 保存处理后的图像至目标路径
                output_image_path = os.path.join(output_class_path, image_name)
                cv2.imwrite(output_image_path, binary_image)

print("已将灰度图像中低于阈值的部分设置为纯黑色，其他部分设置为纯白色，并保存至指定文件夹。")
