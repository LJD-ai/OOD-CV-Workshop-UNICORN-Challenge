import os
import cv2
import numpy as np
import random


def flip_image(image):
    return cv2.flip(image, 1)


def shift_image(image, tx, ty):
    (h, w) = image.shape[:2]
    matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    shifted = cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT_101)
    return shifted


def quarter_crop(image, crop_ratio=0.75):
    (h, w) = image.shape[:2]
    crop_h, crop_w = int(h * crop_ratio), int(w * crop_ratio)

    # 计算裁剪区域的起始坐标
    x = (w - crop_w) // 2
    y = (h - crop_h) // 2

    # 裁剪图像
    cropped = image[y:y + crop_h, x:x + crop_w]
    return cropped


def resize_image(image, size):
    resized = cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)
    return resized


def add_noise(image, noise_factor=0.2):
    noisy_image = image + noise_factor * np.random.normal(size=image.shape)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image


def augment_image(image):
    augmentations = [
        ('flip', flip_image),
        ('shift', lambda img: shift_image(img, 10, 10)),
        ('quarter_crop_resize', lambda img: resize_image(quarter_crop(img), (128, 128))),
        ('noise', add_noise)
    ]

    selected_augmentations = random.sample(augmentations, 2)  # 随机选择两种增强操作

    augmented_images = []
    for name, func in selected_augmentations:
        try:
            augmented_images.append(func(image))
        except ValueError:
            print(f"图像尺寸不足，跳过{name}操作")

    return augmented_images


def process_dataset(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        for filename in files:
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(root, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                # 保存原图
                original_image_path = os.path.join(output_subfolder, filename)
                cv2.imwrite(original_image_path, image)

                # 应用增强并保存增强后的图像
                augmented_images = augment_image(image)

                for i, aug_image in enumerate(augmented_images):
                    output_filename = f"{os.path.splitext(filename)[0]}_aug_{i}.png"
                    output_path = os.path.join(output_subfolder, output_filename)
                    cv2.imwrite(output_path, aug_image)


if __name__ == "__main__":
    input_folder = "./sk_find"  # 替换为你的输入文件夹路径
    output_folder = "./sk_find2"  # 替换为你的输出文件夹路径
    process_dataset(input_folder, output_folder)
