from openai import OpenAI

def deep_seek():
    client = OpenAI(api_key="sk-0e74a967281d4832a0d630f61377ccc9", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system",
             "system": "你是一个数据分析助手，擅长从文本中提取关键信息并进行分析。你的任务是帮助用户理解文档内容，并回答相关问题"},
            {"role": "user", "content": "你好，今天天气怎么样？"},
        ],
        stream=False
    )
    print(response.choices[0].message.content)

    # sk-0e74a967281d4832a0d630f61377ccc9
