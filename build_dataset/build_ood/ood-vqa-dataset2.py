import json

# 读取原始 JSON 文件
with open('train_top_categories_per_image_with_unicorn15000.json', 'r') as file:
    data = json.load(file)

# 生成问题和答案
conversations = []
identity_counter = 0

for item in data:
    image_id = item['image_id']
    file_name = item['file_name']
    top_categories = item['top_categories']

    for obj, count in top_categories.items():
        if count in [0, 1]:
            # 创建问题和答案
            question = f"Is there a {obj} in the image?"
            answer = "Yes" if count == 1 else "No"

            conversation = {
                "id": f"identity_{identity_counter}",
                "conversations": [
                    {
                        "from": "user",
                        "value": f"Picture {1}: <img>/home/pod/shared-nvme/data/train2017/{file_name}</img>\n{question}"
                    },
                    {
                        "from": "assistant",
                        "value": answer
                    }
                ]
            }

            conversations.append(conversation)
            identity_counter += 1

# 将结果保存为新的 JSON 文件
with open('generated_conversations15000_vqa2.json', 'w') as file:
    json.dump(conversations, file, indent=4)

print("处理完成，已生成 generated_conversations15000_vqa2.json 文件。")
