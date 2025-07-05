from request_imag import image_downloader
from image_metadata_processor import ocr_image_to_text, weighted_fusion

class SliderCaptcha():
    def __init__(self):
        # 生成随机版本参数
        self.isg_token = 'BDMz7psnUAwO1h7cHFvSdPXawjddaMcqChuTueXQnNKJ5FKGbTkJeo4ynpQK3x8i'

    def main(self):
        try:
            # 请求图片验证
            captcha_handler = image_downloader.SliderCaptchaHandler()
            captcha_handler.main(self.isg_token)
            # 加权融合为清晰图片
            weighted_fusion.weighted_fusion()
            # 识别清晰图片中文字
            processor = ocr_image_to_text.image_metadata_processor()
            image_text = processor.image_processor()
            print(image_text)
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == '__main__':
    captcha = SliderCaptcha()
    captcha.main()
