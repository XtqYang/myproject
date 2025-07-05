from openai import OpenAI

client = OpenAI(api_key="sk-204ca8732e434845a1437fdae5f64404", base_url="https://api.deepseek.com")

def generate_comment(text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": """小红书美妆区常驻用户，用刷到朋友动态秒回的语气：
                                1. 3句内完成带[表情]的回复 
                                2. 像发语音的自然停顿（用～、...）
                                3. 🚨❗️符号强调重点
                                4. 用生活化类比代替术语
                                5. 允许口语化语病"""
            },
            {"role": "user", "content": f"用户吐槽：{text}"}
        ],
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

# 调用示例
text = "为啥我化出来的妆就感觉没有这种光泽啊[扶额R]而且可以清晰的看见自己的皮肤纹理和毛孔"
print(generate_comment(text))