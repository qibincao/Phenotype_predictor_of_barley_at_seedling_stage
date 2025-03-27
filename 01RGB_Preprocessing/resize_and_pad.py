import os
from PIL import Image

def resize_and_pad(input_folder, output_folder, target_size=512):
    """
    批量将图片补成 1:1 的大小，并更改分辨率到指定大小。
    背景为黑色，图片放置在中心。

    :param input_folder: 输入图片的文件夹路径
    :param output_folder: 输出图片的文件夹路径
    :param target_size: 目标分辨率，默认为 512x512
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 打开图片
            with Image.open(input_path) as img:
                # 获取图片的宽度和高度
                width, height = img.size

                # 如果图片已经是正方形，直接调整大小
                if width == height:
                    img = img.resize((target_size, target_size), Image.ANTIALIAS)
                else:
                    # 计算需要填充的宽度或高度
                    if width > height:
                        new_height = target_size
                        new_width = int(width * (target_size / height))
                    else:
                        new_width = target_size
                        new_height = int(height * (target_size / width))

                    # 调整图片大小
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)

                    # 创建一个黑色背景的图片
                    background = Image.new('RGB', (target_size, target_size), (0, 0, 0))

                    # 计算图片在背景中的位置
                    offset = ((target_size - new_width) // 2, (target_size - new_height) // 2)

                    # 将调整大小后的图片粘贴到背景上
                    background.paste(img, offset)

                    # 保存最终图片
                    background.save(output_path)
                print(f"图片 {filename} 已处理并保存到 {output_path}")

# 示例用法
input_folder = "input"  # 输入图片文件夹路径
output_folder = "output"  # 输出图片文件夹路径
resize_and_pad(input_folder, output_folder)