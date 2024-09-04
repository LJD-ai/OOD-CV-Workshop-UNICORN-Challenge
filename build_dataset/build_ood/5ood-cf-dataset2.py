import json

# 读取之前生成的问答对 JSON 文件
with open('train_generated_qa_pairs15000_vqa.json', 'r') as f:
    qa_pairs = json.load(f)

# 设置图片的根路径
image_root_path = "/home/pod/shared-nvme/data/train2017/"

# 初始化存储对话的列表
conversations = []

# 遍历每个问答对
for idx, qa in enumerate(qa_pairs):
    file_name = qa['file_name']
    question = f"Picture {1}: <img>{image_root_path}{file_name}</img>\n" + qa['question']

    conversation = {
        "id": f"identity_{idx}",
        "conversations": [
            {
                "from": "user",
                "value": question
            },
            {
                "from": "assistant",
                "value": qa['answer']
            }
        ]
    }

    conversations.append(conversation)

# 保存为 JSON 文件
with open('generated_conversations15000_vqa.json', 'w') as f:
    json.dump(conversations, f, indent=4)

print("JSON文件已生成：generated_conversations15000_vqa.json")
