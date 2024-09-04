import os
import requests
from bs4 import BeautifulSoup
import urllib


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_image(url, save_path):
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"Downloaded {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def fetch_images(query, save_directory, num_images=100):
    create_directory(save_directory)
    url = f"https://pic.sogou.com/pics?query={query}&mode=1&start=0&reqType=ajax"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img', limit=num_images)
        for i, img in enumerate(images):
            img_url = img.get('src')
            if img_url:
                save_path = os.path.join(save_directory, f"{query}_{i + 1}.jpg")
                download_image(img_url, save_path)
    else:
        print(f"Failed to retrieve images for {query}")


def main(queries, num_images=100):
    for query in queries:
        save_directory = os.path.join("images", query)
        fetch_images(query, save_directory, num_images)


if __name__ == "__main__":
    queries = [

        "laptop", "moon", "mouth", "present", "radio", "satellite", "ship", "sun", "table", "telephone",
        "train", "tree", "truck", "tv", "van", "wheel"
    ]
    main(queries)
# "angel", "arm", "basket", "bed", "bell", "book", "bowl", "brain", "bridge", "bus", "bush",
# "camera", "cat", "chair", "cup", "diamond", "dog", "door", "eye", "face", "fan", "fish",
# "foot", "guitar", "hand", "hat", "head", "horse", "house", "ipod", "key", "keyboard",