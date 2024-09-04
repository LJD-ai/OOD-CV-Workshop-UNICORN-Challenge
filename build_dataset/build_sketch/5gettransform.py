from PIL import Image, ImageOps
import os
import random
import numpy as np
import cv2

def elastic_transform(image, alpha, sigma, alpha_affine):
    random_state = np.random.RandomState(None)
    shape = image.size[::-1]

    # 仿射变换
    center_square = np.float32(shape) // 2
    square_size = min(shape) // 3
    pts1 = np.float32([center_square + square_size, [center_square[0] + square_size, center_square[1] - square_size], center_square - square_size])
    pts2 = pts1 + random_state.uniform(-alpha_affine, alpha_affine, pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(np.array(image), M, shape, borderMode=cv2.BORDER_REFLECT_101)

    # 弹性变换
    dx = random_state.rand(*shape) * 2 - 1
    dy = random_state.rand(*shape) * 2 - 1
    dx = cv2.GaussianBlur(dx, (0, 0), sigma) * alpha
    dy = cv2.GaussianBlur(dy, (0, 0), sigma) * alpha

    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    map_x = np.float32(x + dx)
    map_y = np.float32(y + dy)

    return Image.fromarray(cv2.remap(np.array(image), map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101))



def perspective_transform(image):
    width, height = image.size
    # 定义原始图像的四个顶点
    original_points = [(0, 0), (width, 0), (width, height), (0, height)]

    # 定义目标图像的四个顶点，随机扰动
    max_shift = 0.2  # 最大的扰动范围，可以调整
    destination_points = [
        (random.uniform(0, width * max_shift), random.uniform(0, height * max_shift)),
        (random.uniform(width * (1 - max_shift), width), random.uniform(0, height * max_shift)),
        (random.uniform(width * (1 - max_shift), width), random.uniform(height * (1 - max_shift), height)),
        (random.uniform(0, width * max_shift), random.uniform(height * (1 - max_shift), height))
    ]

    # 计算透视变换矩阵
    coeffs = find_perspective_coeffs(original_points, destination_points)
    return image.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)


def find_perspective_coeffs(orig_points, dest_points):
    matrix = []
    for p1, p2 in zip(orig_points, dest_points):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(dest_points).reshape(8)

    res = np.linalg.solve(A, B)
    return np.array(res).reshape(8)


def process_image(image_path, save_path):
    # 打开图像
    img = Image.open(image_path)

    # # 随机选择镜像或旋转
    # if random.choice([True, False]):
    #     # 镜像
    #     mirrored_img = ImageOps.mirror(img)
    #     mirrored_img.save(os.path.join(save_path, "mirrored_" + os.path.basename(image_path)))
    # else:
    #     # 旋转
    #     rotated_img = img.rotate(90)  # 旋转90度
    #     rotated_img.save(os.path.join(save_path, "rotated_" + os.path.basename(image_path)))

    # 复杂空间扭曲（透视变换）
    distorted_img = elastic_transform(img, alpha=175, sigma=10, alpha_affine=1)
    distorted_img.save(os.path.join(save_path, "distorted_" + os.path.basename(image_path)))

    # # 保存原图
    # img.save(os.path.join(save_path, "original_" + os.path.basename(image_path)))


def process_images_in_folder(source_folder, target_folder):
    # 遍历每个类别文件夹
    for class_name in os.listdir(source_folder):
        class_path = os.path.join(source_folder, class_name)
        if os.path.isdir(class_path):
            # 创建目标类别文件夹
            target_class_folder = os.path.join(target_folder, class_name)
            if not os.path.exists(target_class_folder):
                os.makedirs(target_class_folder)

            # 处理类别文件夹中的所有图片
            for filename in os.listdir(class_path):
                if filename.endswith(".jpg") or filename.endswith(".png"):  # 添加你数据集中的图片格式
                    image_path = os.path.join(class_path, filename)
                    process_image(image_path, target_class_folder)


# 示例路径
source_folder = "huidu_sk3"  # 替换为你的源文件夹路径
target_folder = "sk_transformed_images"  # 替换为你的目标文件夹路径

# 开始处理图片
process_images_in_folder(source_folder, target_folder)
