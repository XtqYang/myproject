import json
import subprocess
import time
from myproject.utils.m_h5_tk import H5TkExtractor


def _generate_sign(token, page_no, auction_num_id, timestamp, app_key):
    """生成签名"""
    node_path = "./crypto/sign_em.js"
    cmd = ['node', node_path, token, str(page_no), auction_num_id, timestamp, app_key]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result


def generate_signature(auctionNumId, sign, page_no=1, app_key="12574478"):
    """
    生成签名的主函数

    参数:
        auctionNumId: 拍卖ID
        sign: 签名字符串
        page_no: 页码，默认为1
        auction_num_id: 拍卖数字ID，如果不提供则使用auctionNumId
        app_key: 应用密钥，默认为"12574478"

    返回:
        签名结果
    """
    # 初始化H5TkExtractor
    h5_tk_extractor = H5TkExtractor()
    h5_tk_extractor.auctionNumId = auctionNumId
    h5_tk_extractor.sign = sign

    # 获取h5_tk数据
    h5_tk_data = h5_tk_extractor.get_h5_tk()
    token = h5_tk_data[0].split('_')[0]

    # 获取当前时间戳
    timestamp = str(int(time.time() * 1000))

    # 生成签名
    sign_data = _generate_sign(token, page_no, auctionNumId, timestamp, app_key)
    return sign_data


# 使用示例
if __name__ == "__main__":
    auctionNumId = "769361086770"
    sign = "d37e5e17062c5012dddfbdbb09f6af2d"
    result = generate_signature(auctionNumId, sign)
    print(result)
