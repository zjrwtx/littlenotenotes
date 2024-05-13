
import openai
from openai import OpenAI
from dotenv import load_dotenv

import time
import random

from argparse import Namespace
import os
import requests
# 在使用API密钥和基础URL之前加载.env文件
load_dotenv()

API_BASE = os.environ.get("API_BASE")
API_KEY = os.environ.get("API_KEY")
def get_summary(original_url):
    
    client = openai.OpenAI(api_key=API_KEY, base_url=API_BASE)

    reader_url = f"https://r.jina.ai/{original_url}"
    json_response = requests.get(reader_url, headers={"Accept": "application/json"})

    if json_response.status_code == 200:
        json_data = json_response.json()
        markdown_content = f"文档名称:{json_data['data']['title']}\n文档原地址:{json_data['data']['url']}\n{json_data['data']['content']}"

        completion = client.chat.completions.create(
            model="yi-medium-200k",
            max_tokens=20000,
            messages=[{"role": "system", "content":"你是一个文章总结助手，负责将文章内容整理成：一句话总结、重要要点、灵感与启发这三个部分内容"},
                {"role":"user","content":"请按照格式输出为排版美观的纯文本格式：\n\n# 一句话总结\n\n# 重要要点\n\n# 灵感与启发\n\n："+markdown_content},
                ],
        )
        outputtext = completion.choices[0].message.content

   
        return outputtext
    
if __name__ == "__main__":
    print(get_summary("https://mp.weixin.qq.com/s/v6xvH1uPq8W5osws_yUzWg"))