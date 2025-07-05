import os

from paddleocr import PaddleOCR
import logging
# 禁用所有INFO及以下级别的日志
logging.disable(logging.INFO)

class image_metadata_processor():
    def __init__(self):
        # 初始化 OCR，指定语言为中文
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        self.output_dir = (os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
        self.image_path = fr"{self.output_dir}\images\result.jpg"
        # 如果未指定输出目录，默认使用当前脚本所在目录的 images 子目录

    def image_processor(self):
        # 识别图片中的文字
        texts = []
        result = self.ocr.ocr(self.image_path, cls=True)
        # 解析并输出识别的文本
        for line in result:
            for word_info in line:
                text = word_info[1][0]  # 识别出的文字
                texts.append(text)
                confidence = word_info[1][1]  # 置信度
                # print(f"识别内容: {text} | 置信度: {confidence:.2f}")
            # 合并为自然段落（根据中文排版习惯不加空格）
        combined_text = ''.join(texts)
        return combined_text
#
# if __name__ == "__main__":
#     processor = image_metadata_processor()
#     image_processor = processor.image_processor()
#     print(image_processor)
