import json
import re

# 汉字的 Unicode 范围
hanzi_pattern = re.compile(u'[\u4e00-\u9fff]')

def contains_hanzi(text):
    return bool(hanzi_pattern.search(text))

# 读取 JSON 文件
with open('sk_vqa_find_cf2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 检查 JSON 中的所有字符串是否包含汉字
def check_json_for_hanzi(obj):
    if isinstance(obj, str):
        return contains_hanzi(obj)
    elif isinstance(obj, dict):
        return any(check_json_for_hanzi(value) for value in obj.values())
    elif isinstance(obj, list):
        return any(check_json_for_hanzi(item) for item in obj)
    return False

if check_json_for_hanzi(data):
    print("JSON 文件中包含汉字。")
else:
    print("JSON 文件中不包含汉字。")
