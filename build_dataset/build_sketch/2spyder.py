import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random


# 创建保存图片的文件夹
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# 从Bing搜索图片
def search_bing_images(query, num_images=100):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    search_query = f"{query} 简笔画"
    url = f"https://www.bing.com/images/search?q={search_query}&FORM=HDRSC2"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []

    for img in soup.find_all('img', limit=num_images * 2):  # 尝试获取更多的图片链接
        img_url = img.get('src') or img.get('data-src')
        if img_url and img_url.startswith('http'):
            images.append(img_url)
        if len(images) >= num_images:
            break

    return images


# 下载图片
def download_images(images, directory, query):
    create_directory(directory)
    for idx, img_url in enumerate(images):
        try:
            img_data = requests.get(img_url).content
            with open(os.path.join(directory, f"{query}_{idx + 1}.jpg"), 'wb') as img_file:
                img_file.write(img_data)
            print(f"Downloaded: {query}_{idx + 1}.jpg")
        except Exception as e:
            print(f"Could not download image {idx + 1} for query {query}. Error: {e}")


# 主函数
def main(queries, num_images=100):
    base_directory = 'bing_simplified_drawings_cf'
    create_directory(base_directory)

    for query in queries:
        sub_directory = os.path.join(base_directory, query)
        print(f"Searching for images of: {query} 简笔画")
        images = search_bing_images(query, num_images)
        if images:
            download_images(images, sub_directory, query)
        else:
            print(f"No images found for: {query} 简笔画")

        # 增加随机延时，减少触发反爬机制的可能性
        time.sleep(random.uniform(1, 3))


if __name__ == "__main__":
    queries = [
        "armchair", "ashtray", "bathtub", "blimp", "boomerang", "bulldozer", "carrot",
        "chandelier", "crocodile", "donut", "eyeglasses", "giraffe", "grenade", "hamburger",
        "hedgehog", "hourglass", "kangaroo", "lightbulb", "loudspeaker", "megaphone",
        "mermaid", "motorbike", "octopus", "parachute", "pretzel", "revolver", "rollerblades",
        "rooster", "sailboat", "saxophone", "scorpion", "screwdriver", "seagull", "shovel",
        "skateboard", "skyscraper", "snail", "snowman", "squirrel", "stapler", "streetlight",
        "suitcase", "syringe", "teacup", "teapot", "toothbrush", "trombone", "wheelbarrow",
        "windmill", "wineglass"
    ]

    main(queries)
# "angel", "arm", "basket", "bed", "bell", "book", "bowl", "brain",
# "bridge", "bus", "bush", "camera", "cat", "chair", "cup", "diamond",
# "dog", "door", "eye", "face", "fan", "fish", "foot", "guitar", "hand",
# "hat", "head", "horse", "house", "ipod", "key", "keyboard",