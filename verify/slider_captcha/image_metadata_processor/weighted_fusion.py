import os

import cv2


def weighted_fusion():
    output_dir = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__))))
    print(output_dir)
    # 读取图像
    frame1 = cv2.imread(fr"{output_dir}\images\text1.jpg")
    frame2 = cv2.imread(fr"{output_dir}\images\text2.jpg")
    # 检查是否成功读取图像
    if frame1 is None or frame2 is None:
        print("Error: 图片未找到！")
        exit()

    # 加权融合（可调节alpha值）
    blended = cv2.addWeighted(frame1, 0.5, frame2, 0.5, 0)

    # 保存图像
    cv2.imwrite(fr"{output_dir}\images\result.jpg", blended)
    print("图片已保存为 ../images/result.jpg")


if __name__ == "__main__":
    weighted_fusion()