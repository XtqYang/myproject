import os
import warnings
import requests
import base64
import json
import random
from io import BytesIO
from PIL import Image
from typing import Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.WARNING)


class SliderCaptchaHandler:
    def __init__(self):
        # 如果未指定输出目录，默认使用当前脚本所在目录的 images 子目录
        self.output_dir = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__))))

        # 常量定义
        self.REQUEST_COOKIES = {
            'lid': 'tb528238846663',
            'cookie3_bak': '17af0ee9c37ba35e43e3ca54a8cebd2f',
            'env_bak': 'FM%2Bgm%2FLsLU9A4rJ1FgHP60VCPlEfNzKsIK%2B1NLhtfUD5',
            'wk_unb': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            'wk_cookie2': '151177e5c67f84d11997af48b49e9de2',
            'cookie3_bak_exp': '1742114742462',
            'havana_lgc_exp': '1772965846161',
            '_l_g_': 'Ug%3D%3D',
            'lgc': 'tb528238846663',
            'cookie1': 'BdTujoy%2Fv745d0Ov9DgOHFMLNMtwU4xV7thGHePIEH4%3D',
            'login': 'true',
            'cookie2': '17af0ee9c37ba35e43e3ca54a8cebd2f',
            'cancelledSubSites': 'empty',
            'sg': '308',
            'sn': '',
            '_tb_token_': '58e33aa81eba5',
            'dnk': 'tb528238846663',
            'uc3': 'nk2=F5RAQIcpOqF0wFxodeQ%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&vt3=F8dD2EjME%2BYP7XAx3uc%3D&id2=UUpgT7v9r1VNs0K1OQ%3D%3D',
            'tracknick': 'tb528238846663',
            'uc4': 'nk4=0%40FY4L7HgyQ01YvoqPicBCi%2BYt%2FDt%2Fh4xCoA%3D%3D&id4=0%40U2gqwARzFIUfVaMSaLM2EjsVPTbtaxjC',
            'unb': '2219453037520',
            'cookie17': 'UUpgT7v9r1VNs0K1OQ%3D%3D',
            '_nk_': 'tb528238846663',
            'sgcookie': 'E1004cA73k5ovrB%2Fi1Jh%2BTylMpULGEILR8V6W7QrMRyavuHgtP5mGQktvgNtNfs4UxblrFTOCGdQeM7eOM0bWYzT1kVya8eRXRGwKiC0wjYXNYk%3D',
            't': '20c1b8c96e003a04455d570c7d82bc72',
            'csg': '1107a33b',
            'havana_sdkSilent': '1741952221075',
            'cna': 'Bn1NIIRCWV8BASQKQs0iQwHG',
            'x5sectag': '682138',
            'isg': None  # 留空以便动态填充
        }

        self.REQUEST_HEADERS = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://h5api.m.tmall.com//h5/mtop.taobao.pcdetail.data.get/1.0/_____tmd_____/punish?x5secdata=xd382657694a2ce86ae086c50981ce08e5061f0053ff4d97e31742107914a-717315356a683744249abaac3en2219453037520kcapslidev2__bx__h5api.m.tmall.com%3A443%2Fh5%2Fmtop.taobao.pcdetail.data.get%2F1.0&x5step=2&action=captchacapslidev2&pureCaptcha=',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }

        self.BASE_PARAMS = {
            'token': '6b5080c0d01a1e01d7d86bb740efcf18',
            'appKey': 'X82Y__d366b44467147323c70b42d8a2d852f5',
            'x5secdata': 'xd4160a0cb2ded97246b5080c0d01a1e01d7d86bb740efcf181742114527a-717315356a683744249abaac3en2219453037520kcapslidev2__bx__h5api.m.tmall.com:443/h5/mtop.taobao.pcdetail.data.get/1.0',
            'language': 'cn',
            'v': None  # 留空以便动态填充
        }

        self.API_ENDPOINT = 'https://h5api.m.tmall.com/h5/mtop.taobao.pcdetail.data.get/1.0/_____tmd_____/newslidecaptcha'

    def fetch_image_data(self, isg_token: str, version_param: str) -> requests.Response:
        """
        获取图片数据API请求
        :param isg_token: ISG令牌参数
        :param version_param: 版本参数
        :return: 请求响应对象
        """
        try:
            # 动态更新请求参数
            dynamic_cookies = self.REQUEST_COOKIES.copy()
            dynamic_cookies['isg'] = isg_token

            dynamic_params = self.BASE_PARAMS.copy()
            dynamic_params['v'] = version_param

            response = requests.get(
                self.API_ENDPOINT,
                params=dynamic_params,
                cookies=dynamic_cookies,
                headers=self.REQUEST_HEADERS,
                timeout=10
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API请求失败: {str(e)}")

    def save_base64_image(self, base64_str: str, filename: str, image_type: str = 'auto') -> None:
        """
        保存Base64编码的图片到文件
        :param base64_str: 完整Base64字符串（包含前缀）
        :param filename: 保存文件名（不带扩展名）
        :param image_type: 指定图片类型（jpg/png/auto）
        """
        try:
            # 分离元数据和图片数据
            meta, data = base64_str.split(",", 1)

            # 自动检测图片类型
            if image_type == 'auto':
                if 'jpeg' in meta or 'jpg' in meta:
                    file_ext = 'jpg'
                elif 'png' in meta:
                    file_ext = 'png'
                else:
                    raise ValueError("不支持的图片格式")
            else:
                file_ext = image_type

            img_bytes = base64.b64decode(data)
            Image.open(BytesIO(img_bytes)).save(f"{filename}.{file_ext}")
        except (ValueError, IOError) as e:
            raise RuntimeError(f"图片保存失败: {str(e)}")

    def process_response_data(self, response_data: Dict[str, Any]) -> None:
        """
        处理API返回的图片数据
        :param response_data: 解析后的JSON数据
        """
        try:
            # 处理主图
            main_image_data = response_data["data"]["imageData"]
            # 处理2张分图片
            ques_data = response_data["data"]["ques"].split("|")
            if len(ques_data) >= 2:
                self.save_base64_image(main_image_data, fr"{self.output_dir}\images\main_image")
                for idx, img_data in enumerate(ques_data[1:], start=1):  # 跳过第一个元素
                    self.save_base64_image(img_data, fr"{self.output_dir}\images\text{idx}")
                print("图片保存成功")
                print(f"保存路径:{self.output_dir}\images")
            else:
                logging.warning(f"ques只有{len(ques_data)}张base图片,请修改cookie和params信息")
        except KeyError as e:
            raise RuntimeError(f"响应数据缺少关键字段: {str(e)}")

    def main(self, isg_token):
        version_param = str(random.random()).replace('.', '')

        try:
            # 获取数据
            response = self.fetch_image_data(isg_token, version_param)
            print("原始响应数据:", response.text)

            # 处理数据
            json_data = json.loads(response.text)
            self.process_response_data(json_data)

        except (json.JSONDecodeError, RuntimeError) as e:
            print(f"处理失败: {str(e)}")


if __name__ == "__main__":
    isg_token = 'BOnpzfu2qs43vpR-MtV4dvPM-JVDtt3ozE2Zm4veQ1APUghk0weNuMoEFHbkUXUg'
    handler = SliderCaptchaHandler()
    handler.main(isg_token)
