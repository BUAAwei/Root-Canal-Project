import matplotlib.pyplot as plt
from torchvision import transforms
from PIL import Image

# 假设 original_image 是一个 PIL Image 对象
original_image = Image.open("./data/imgs/1.png")

# 定义图像变换操作
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),  # 随机水平翻转
    transforms.RandomVerticalFlip(p=0.5),  # 随机垂直翻转
    transforms.RandomResizedCrop((695, 695), scale=(0.5, 1), ratio=(0.5, 2))
    # 其他变换操作...
])

# 应用变换操作
augmented_image = transform(original_image)

# 将 PIL Image 转为 PyTorch 的 Tensor
augmented_image_tensor = transforms.ToTensor()(augmented_image)

plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.imshow(original_image)

plt.subplot(1, 2, 2)
plt.imshow(augmented_image)