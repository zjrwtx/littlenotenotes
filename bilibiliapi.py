import openai
from openai import OpenAI
from dotenv import load_dotenv

import time
import random

import asyncio
from bilix.sites.bilibili import DownloaderBilibili
from bcut_asr_branch import run_everywhere
from argparse import Namespace
import os


def get_bilibili_summary(original_url):

            try:
                async def main():
                    async with DownloaderBilibili() as downloader:
                        # 下载视频并获取文件名
                        await downloader.get_video(original_url)
                        # 设置包含视频文件的文件夹路径
                        video_folder_path = './'

                        # 遍历文件夹中的所有文件
                        for filename in os.listdir(video_folder_path):
                            # 检查文件扩展名是否为视频文件，这里我们假设视频文件扩展名为.mp4
                            if filename.endswith('.mp4'):
                                # 构建完整的文件路径
                                file_path = os.path.join(video_folder_path, filename)
                                
                                # 打开视频文件
                                with open(file_path, "rb") as f:
                                    # 创建Namespace对象，设置参数
                                    argg = Namespace(format="txt", interval=15.0, input=f, output=None)
                                    
                                    # 运行语音识别并生成字幕
                                    run_everywhere(argg)
                asyncio.run(main())

            except Exception as e:
                print(f"An error occurred: {e}")


            # 指定要遍历的文件夹路径
            folder_path = './'

            # 遍历文件夹中的文件
            for filename in os.listdir(folder_path):
                # 检查文件扩展名是否为.txt
                if filename.endswith('.txt'):
                    # 构建完整的文件路径
                    file_path = os.path.join(folder_path, filename)
                    # 打开文件并进行操作
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # 这里可以添加读取文件内容的代码
                        content = file.read()
                        print(f'文件 {filename} 的内容是：')
                        print(content)


            # 在使用API密钥和基础URL之前加载.env文件
            load_dotenv()

            # 现在可以通过os.environ访问这些值
            API_BASE = os.environ.get("API_BASE")
            API_KEY = os.environ.get("API_KEY")


            client = OpenAI(
                # defaults to os.environ.get("OPENAI_API_KEY")
                api_key=API_KEY,
                base_url=API_BASE
            )
            completion = client.chat.completions.create(
                model="yi-medium-200k",
                
                messages=[{"role": "system", "content":"你是一个文章总结助手，负责将文章内容整理成：一句话总结、重要要点、灵感与启发这三个部分内容"},
                {"role":"user","content":"请按照格式输出为排版美观的纯文本格式：\n\n# 一句话总结\n\n# 重要要点\n\n# 灵感与启发\n\n："+content},
                ],
                max_tokens=6000,
                top_p=0.8,
                # stream=True,
            )
            outputtext=completion.choices[0].message.content
            return outputtext

if __name__=="__main__":
    get_bilibili_summary("https://www.bilibili.com/video/BV1gC41177xR/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=5531fb0981ef79f87198a3c2651dff93")

# for chunk in completion:
#     # print(chunk) 
#     print(chunk.choices[0].delta.content or "", end="", flush=True)


# https://www.youtube.com/watch?v=CjTTSa33axg