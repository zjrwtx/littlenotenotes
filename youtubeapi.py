import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

import time
import random
from youtube_transcript_api import YouTubeTranscriptApi

# 在使用API密钥和基础URL之前加载.env文件
load_dotenv()

# 现在可以通过os.environ访问这些值
API_BASE = os.environ.get("API_BASE")
API_KEY = os.environ.get("API_KEY")

def get_youtube_summary(original_url):
        client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=API_KEY,
            base_url=API_BASE
        )
        try:
            video_id = original_url.split("=")[1]
            # Fetch the transcript
            print(video_id)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

        except Exception as e:
            print(f"An error occurred: {e}")

        #merge all the text in one string
        text = ""
        for i in transcript:
            text += i['text'] + " "

        completion = client.chat.completions.create(
            model="yi-medium-200k",
             messages=[{"role": "system", "content":"你是一个文章总结助手，负责将文章内容整理成：一句话总结、重要要点、灵感与启发这三个部分内容"},
                {"role":"user","content":"请按照格式输出为排版美观的纯文本格式：\n\n# 一句话总结\n\n# 重要要点\n\n# 灵感与启发\n\n："+text},
                ],
            max_tokens=6000,
            top_p=0.8,
            # stream=True,
        )
        outputtext=completion.choices[0].message.content
        return outputtext


if __name__ == "__main__":
    print(get_youtube_summary("https://www.youtube.com/watch?v=H4VpVMKx19k"))

# for chunk in completion:
#     # print(chunk) 
#     print(chunk.choices[0].delta.content or "", end="", flush=True)


# https://www.youtube.com/watch?v=CjTTSa33axg