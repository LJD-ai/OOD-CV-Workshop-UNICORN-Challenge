import os
import random
import json

# 定义z文件夹路径
z_dir = './sk_find2'
root_path = '/home/pod/shared-nvme/data/sk_find2'  # 根路径，需替换为实际图片根路径

# 获取z文件夹中的所有物体名称（假设物体名称为文件夹名称）
object_names = os.listdir(z_dir)

# 定义问题模板
question_templates = [
    "<img>{}</img>\nIs this a {} in the image?",
    "<img>{}</img>\nIs there a sketchy {} in the picture?",
    "<img>{}</img>\nIn the scene, is a {} in it?"
]

# 初始化结果列表
qa_data = []
id_counter = 0  # 用于生成唯一的id

# 遍历z文件夹中的每个物体
for obj_name in object_names:
    # 获取该物体类别文件夹中的所有图片文件
    obj_dir = os.path.join(z_dir, obj_name)
    image_files = os.listdir(obj_dir)

    half_image=len(image_files)//4
    selected_images = random.sample(image_files,half_image)

    for image_file in image_files:
        # 图片的完整路径
        image_path = os.path.join(root_path, obj_name, image_file)

        # 为当前图片选择一个问题模板
        chosen_template_yes = random.choice(question_templates)
        question_yes = chosen_template_yes.format(image_path,obj_name)
        answer_yes = "Yes"

        # 为当前图片随机选择其他类别名称
        other_names = [name for name in object_names if name != obj_name]
        random_other_name = random.choice(other_names)
        chosen_template_no = random.choice(question_templates)
        question_no = chosen_template_no.format(image_path,random_other_name)
        answer_no = "No"

        # 构建第一个对话
        conversations_yes = [
            {"from": "user", "value": question_yes},
            {"from": "assistant", "value": answer_yes}
        ]

        qa_data.append({
            "id": f"identity_{id_counter}",
            "conversations": conversations_yes
        })
        id_counter += 1

        # 构建第二个对话
        conversations_no = [
            {"from": "user", "value": question_no},
            {"from": "assistant", "value": answer_no}
        ]

        qa_data.append({
            "id": f"identity_{id_counter}",
            "conversations": conversations_no
        })
        id_counter += 1

# 保存为JSON文件
output_file = 'sk_find2.json'
with open(output_file, 'w') as f:
    json.dump(qa_data, f, indent=2, ensure_ascii=False)

print(f"问答对已生成并保存到 {output_file}")