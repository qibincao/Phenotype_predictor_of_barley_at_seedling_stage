import os
import rasterio
from rasterio.windows import Window
from PIL import Image, ImageEnhance
import numpy as np
import warnings

print("当前工作目录:", os.getcwd())
# 忽略没有地理参考的警告
warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)

def combine_images_to_rgb(image_paths):
    # 打开三张图像并转换为 NumPy 数组
    image1 = np.array(Image.open(image_paths[0]).convert("L"))  # 转换为灰度图像
    image2 = np.array(Image.open(image_paths[1]).convert("L"))
    image3 = np.array(Image.open(image_paths[2]).convert("L"))

    # 确保所有图像大小相同
    if image1.shape != image2.shape or image2.shape != image3.shape:
        raise ValueError("All images must have the same size")

    # 合成 RGB 图像
    combined_image = np.stack((image1, image2, image3), axis=-1)
    return Image.fromarray(combined_image, mode="RGB")

def adjust_image(image, contrast_factor=1.5, brightness_factor=1.2):
    """
    调整图像的对比度和亮度
    :param image: PIL 图像对象
    :param contrast_factor: 对比度因子（>1 增加对比度，<1 降低对比度）
    :param brightness_factor: 亮度因子（>1 增加亮度，<1 降低亮度）
    :return: 调整后的图像
    """
    # 调整对比度
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)

    # 调整亮度
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)

    return image

def process_dataset(input_dir, output_dir, bands):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录的所有子文件夹和文件
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".dat"):
                dat_path = os.path.join(root, file)
                hdr_path = dat_path.replace(".dat", ".hdr")
                if not os.path.exists(hdr_path):
                    print(f"Warning: Missing HDR file for {dat_path}. Skipping...")
                    continue

                try:
                    with rasterio.open(dat_path) as dataset:
                        for band_number in bands:
                            data = dataset.read(band_number)
                            data = ((data - data.min()) / (data.max() - data.min()) * 255).astype(np.uint8)

                            # 创建图像并保存
                            img = Image.fromarray(data)
                            output_filename = os.path.splitext(file)[0] + f"_band_{band_number}.jpg"
                            img.save(os.path.join(output_dir, output_filename))

                        # 检查是否已经处理了所有三个波段
                        if all(os.path.exists(os.path.join(output_dir, f"{os.path.splitext(file)[0]}_band_{b}.jpg")) for b in bands):
                            # 合成图像
                            image_paths = [os.path.join(output_dir, f"{os.path.splitext(file)[0]}_band_{b}.jpg") for b in bands]
                            combined_image = combine_images_to_rgb(image_paths)

                            # 调整对比度和亮度
                            combined_image = adjust_image(combined_image, contrast_factor=3.0, brightness_factor=2.2)

                            combined_filename = os.path.splitext(file)[0] + "_combined.jpg"
                            combined_image.save(os.path.join(output_dir, combined_filename))

                            # 删除单波段图像
                            for b in bands:
                                band_filename = os.path.join(output_dir, f"{os.path.splitext(file)[0]}_band_{b}.jpg")
                                os.remove(band_filename)

                            # 重命名合成图像
                            os.rename(os.path.join(output_dir, combined_filename), os.path.join(output_dir, os.path.splitext(file)[0] + ".jpg"))
                except Exception as e:
                    print(f"Error processing {dat_path}: {e}")

# 输入目录
input_dir = "input"
# 输出目录
output_dir = "output"
# 要提取的波段
bands = [70, 53, 19]

process_dataset(input_dir, output_dir, bands)