import json
import random

# 读取修改后的 JSON 文件
with open('train_top_categories_per_image_with_unicorn15000.json', 'r') as f:
    data = json.load(f)
number_to_words = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
21: "twentyone",
22: "twentytwo",
24: "twentyfour",
25: "twentyfive",
26: "twentysix",
27: "twentyseven",
28: "twentyeight"
}

# 初始化存储问题和答案的列表
qa_pairs = []

# 定义新的句式
add_phrases = [
    "How many {category}s are there in the image?",
]


# 遍历每张图片的数据
for image_data in data:
    file_name = image_data['file_name']
    categories = image_data['top_categories']

    # 遍历每个类别，生成问题和答案
    for category, count in categories.items():
        correct_answer = count
        offset = random.choice([-2, -1, 1, 2])
        incorrect_answer = correct_answer + offset

        # 确保错误答案在合理范围内
        while incorrect_answer < 0 or incorrect_answer > 28:  # 根据实际需要调整范围
            offset = random.choice([-2, -1, 1, 2])
            incorrect_answer = correct_answer + offset

        phrase = random.choice(add_phrases)
        question = (f"In the given image, it is known that there are either {correct_answer} or {incorrect_answer} {category}s. "
                    f"{phrase.format(category=category)}"
                    f"Attention : Choose the answer from {correct_answer} and {incorrect_answer}.")
        # question = ("How many {category}(s) would there be in the image now that {change} more {category}(s) have been moved into the scene?")
        answer = f"{correct_answer}"

        # 将问题和答案添加到列表中
        qa_pairs.append({
            'file_name': file_name,
            'question': question,
            'answer': answer
        })

# 保存问题和答案为 JSON 文件
with open('train_generated_qa_pairs15000_vqa.json', 'w') as f:
    json.dump(qa_pairs, f, indent=4)

print("JSON文件已生成：train_generated_qa_pairs15000_vqa.json")
