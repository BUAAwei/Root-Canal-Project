from PIL import Image
import os
import random

input_folder = r".\data\imgs"
mask_folder = r".\data\masks"
output_img_folder = r".\data\processed_img\img"
output_mask_folder = r".\data\processed_img\msk"

if not os.path.exists(output_img_folder):
    os.makedirs(output_img_folder)
if not os.path.exists(output_mask_folder):
    os.makedirs(output_mask_folder)

image_files = [f for f in os.listdir(input_folder) if f.endswith(".png") or f.endswith(".jpg")]

for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    mask_path = os.path.join(mask_folder, image_file)

    image = Image.open(image_path)
    mask = Image.open(mask_path)

    # 水平翻转
    flip_horizontal_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    flip_horizontal_mask = mask.transpose(Image.FLIP_LEFT_RIGHT)

    output_image_file = os.path.join(output_img_folder, f"{os.path.splitext(image_file)[0]}_flip_horizontal.png")
    output_mask_file = os.path.join(output_mask_folder, f"{os.path.splitext(image_file)[0]}_flip_horizontal.png")

    flip_horizontal_image.save(output_image_file)
    flip_horizontal_mask.save(output_mask_file)

    # 竖直翻转
    flip_vertical_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    flip_vertical_mask = mask.transpose(Image.FLIP_TOP_BOTTOM)

    output_image_file = os.path.join(output_img_folder, f"{os.path.splitext(image_file)[0]}_flip_vertical.png")
    output_mask_file = os.path.join(output_mask_folder, f"{os.path.splitext(image_file)[0]}_flip_vertical.png")

    flip_vertical_image.save(output_image_file)
    flip_vertical_mask.save(output_mask_file)

    # 旋转
    for i in range(1, 12):
        angle = 30 * i
        rotated_image = image.rotate(angle, expand=False)
        rotated_mask = mask.rotate(angle, expand=False)

        output_image_file = os.path.join(output_img_folder, f"{os.path.splitext(image_file)[0]}_rotate_{angle}.png")
        output_mask_file = os.path.join(output_mask_folder, f"{os.path.splitext(image_file)[0]}_rotate_{angle}.png")

        rotated_image.save(output_image_file)
        rotated_mask.save(output_mask_file)

    # 裁切
    for i in range(1, 4):
        width, height = image.size
        left = random.randint(0, 294)
        upper = random.randint(0, 294)
        right = left + 400
        lower = upper + 400

        cropped_image = image.crop((left, upper, right, lower))
        restored_image = cropped_image.resize((width, height))
        cropped_mask = mask.crop((left, upper, right, lower))
        restored_mask = cropped_mask.resize((width, height))

        output_image_file = os.path.join(output_img_folder, f"{os.path.splitext(image_file)[0]}_random_crop_{i}.png")
        output_mask_file = os.path.join(output_mask_folder, f"{os.path.splitext(image_file)[0]}_random_crop_{i}.png")

        restored_image.save(output_image_file)
        restored_mask.save(output_mask_file)
