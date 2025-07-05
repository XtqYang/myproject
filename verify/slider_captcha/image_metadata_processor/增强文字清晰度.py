import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取图片
image_path = "blended_output.jpg"
image = cv2.imread(image_path)

# 检查是否成功读取图片
if image is None:
    raise ValueError("无法读取图片，请检查文件路径")

# 转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用高斯模糊去噪
denoised = cv2.GaussianBlur(gray, (3, 3), 0)

# 进行锐化处理
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
sharpened = cv2.filter2D(denoised, -1, kernel)

# 直方图均衡化，提高对比度
equalized = cv2.equalizeHist(sharpened)

# 保存处理后的图片
output_path = "enhanced_output.jpg"
cv2.imwrite(output_path, equalized)

# 显示原图和处理后的图像
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(gray, cmap='gray')
plt.title("原始图片")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(equalized, cmap='gray')
plt.title("增强后的图片")
plt.axis("off")

plt.show()
