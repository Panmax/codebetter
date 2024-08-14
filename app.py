import os
import openai
import gradio as gr

# 设置 OpenAI API 密钥
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key for OpenAI is not set. Please set the 'OPENAI_API_KEY' environment variable.")
client = openai.OpenAI(api_key=api_key)


def optimize_code(code):
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=102400,
        temperature=0.4,
        stream=True,
        messages=[
            {
                "role": "system",
                "content": "You are a senior software enginner."
            },
            {
                "role": "user",
                "content": "帮我优化以下代码并修复可能存在的bug，请先写代码，再使用中文解释修改原因。"
                           "如果优化后的代码足够优雅，我将奖励你1000美金作为小费。"
            },
            {
                "role": "user",
                "content": code
            }
        ],
    )

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message


iface = gr.Interface(
    fn=optimize_code,
    inputs="textbox",
    outputs="markdown",
    title="Code Better",
    description="Talk is cheap, Show me the code:",
    allow_flagging='never',
    css="footer{display:none !important}",
)

iface.launch()
