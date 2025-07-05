import json

from openpyxl import load_workbook
from openai import OpenAI
import time


def process_text_with_deepseek(text):
    """使用DeepSeek处理文本并返回结构化结果"""
    client = OpenAI(
        api_key="sk-0e74a967281d4832a0d630f61377ccc9",
        base_url="https://api.deepseek.com"
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个专业的产品分析助手，请严格按以下要求工作：
                                1. 始终使用简体中文输出
                                2. 分析时必须包含：优点、缺点、核心卖点、改进建议
                                3. 输出格式必须为严格JSON格式：
                                {
                                  "优点": "15字左右的要点",
                                  "缺点": "15字左右的客观缺陷",
                                  "核心卖点": "最具竞争力的产品特征",
                                  "改进建议": "具体的优化方向建议"
                                }"""
                },
                {
                    "role": "user",
                    "content": f"产品描述：{text}\n请按指定格式输出分析结果，不要任何解释说明"
                }
            ],
            stream=False,
            temperature=0.1,  # 降低随机性确保格式稳定
            # response_format={ "type": "json_object" }  # 如果API支持JSON模式
        )

        # 格式校验
        result = response.choices[0].message.content.strip()
        if not result.startswith("{"):
            result = result[result.find("{"):]  # 去除可能的前缀
        return result

    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return json.dumps({
            "优点": "解析失败",
            "缺点": "解析失败",
            "核心卖点": "解析失败",
            "改进建议": "解析失败"
        }, ensure_ascii=False)


# 加载Excel文件（建议先备份原始文件）
workbook = load_workbook(r'D:\file\影刀数据表格.xlsx')
sheet = workbook.active

# 从第2行开始处理（假设第1行是标题）
start_row = 1
e_column = 5  # E列是第5列
for row in range(start_row, sheet.max_row + 1):
    # for row in range(26, 30):
    original_text = sheet.cell(row=row, column=e_column).value

    if original_text:  # 仅处理有内容的单元格
        print(f"正在处理第{row}行...")
        print("一定要使用中文回复，直接给我结果不要给我分析过程,将后面这段话的评价浓缩为10字左右的文本:" + original_text)
        # 调用处理函数
        processed_text = process_text_with_deepseek(original_text)

        # 写入处理结果
        sheet.cell(row=row, column=e_column).value = processed_text

        # 添加延时避免速率限制（根据API限制调整）
        time.sleep(1)

# 另存为新文件避免覆盖原始数据
workbook.save(r'D:\file\影刀数据表格_processed.xlsx')
print("处理完成，结果已保存到新文件")
