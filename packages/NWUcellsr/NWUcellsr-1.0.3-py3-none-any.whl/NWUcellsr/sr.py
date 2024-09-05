import torch
from PIL import Image
from io import BytesIO
from torchvision import transforms
from craft_arch import CRAFT  # 替换为你的模型类

# 加载模型
model = CRAFT()
model.load_state_dict(torch.load('sr.pth'), strict=False)
model.eval()

# 预处理函数
def transform(img):
    transform_pipeline = transforms.Compose([
        transforms.Resize((96, 96)),  # 根据模型输入要求调整大小
        transforms.ToTensor(),          # 将 PIL 图像转换为张量
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # 归一化
    ])
    return transform_pipeline(img)

def transform_back(tensor):
    # 将张量反归一化
    tensor = tensor * 0.5 + 0.5  # 假设原始数据范围是 [0, 1]
    tensor = tensor.clamp(0, 1)  # 确保值在 [0, 1] 之间
    tensor = transforms.ToPILImage()(tensor)  # 转换为 PIL 图像
    return tensor

def process_image(img_file):
    # 将图像文件读取为 PIL 图像
    img = Image.open(BytesIO(img_file.read()))

    # 将图像转换为张量（根据你的模型要求进行适当的预处理）
    img_tensor = transform(img).unsqueeze(0)  # 添加 batch 维度

    # 使用模型进行预测
    with torch.no_grad():
        output = model(img_tensor)

    # 处理模型输出（将张量转换回图像等）
    output_img = output.squeeze(0)  # 移除 batch 维度
    output_img = transform_back(output_img)  # 逆变换为图像

    # 保存处理后的图像
    output_image_path = 'results/output_image.png'
    output_img.save(output_image_path)

    return output_image_path
