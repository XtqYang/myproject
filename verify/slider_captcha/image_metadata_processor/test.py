import cv2
import numpy as np


def motion_deblur(blur1, blur2):
    """
    运动模糊反卷积融合算法
    输入：两张不同方向的运动模糊图片
    输出：去模糊后的图像
    """
    # 转换为浮点型进行计算
    blur1 = cv2.cvtColor(blur1, cv2.COLOR_BGR2GRAY).astype(np.float32)
    blur2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2GRAY).astype(np.float32)

    # 傅里叶变换
    f1 = np.fft.fft2(blur1)
    f2 = np.fft.fft2(blur2)

    # 计算频域平均
    f_combined = 0.5 * (np.abs(f1) + np.abs(f2)) * np.exp(1j * (np.angle(f1) + np.angle(f2)) / 2)

    # 逆傅里叶变换
    recovered = np.fft.ifft2(f_combined).real

    # 后处理
    recovered = np.clip(recovered, 0, 255).astype(np.uint8)
    return cv2.cvtColor(recovered, cv2.COLOR_GRAY2BGR)


# 使用示例
img1 = cv2.imread("../images/text1.jpg")
img2 = cv2.imread("../images/text2.jpg")
result = motion_deblur(img1, img2)
cv2.imwrite("../images/result.jpg", result)
print("静态清晰图片已保存: ../imagesdeblurred_result.jpg")