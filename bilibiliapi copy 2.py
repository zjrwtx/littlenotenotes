import asyncio
from bilix.sites.bilibili import DownloaderBilibili
from bcut_asr_branch import run_everywhere
from argparse import Namespace
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
from deletevideos import delete_videos_from_folder
from deletesrttxt import deletesrttxt_from_folder
def get_bilibili_summary(original_url):
    
    # 首先加载环境变量
    load_dotenv()
    API_BASE = os.environ.get("API_BASE")
    API_KEY = os.environ.get("API_KEY")

    # 初始化OpenAI客户端
    client = OpenAI(
        api_key=API_KEY,
        base_url=API_BASE
    )

    async def download_and_transcribe():
        try:
         
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
                            argg = Namespace(format="txt", interval=15.0, input=f, output="./srtoutput")
                            
                            # 运行语音识别并生成字幕
                            run_everywhere(argg)
                          # 删除视频
                        delete_videos_from_folder(video_folder_path)

                # 指定要遍历的文件夹路径
                folder_path = './srtoutput'

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
                        deletesrttxt_from_folder(folder_path)

                # 准备发送给OpenAI API的请求内容
                request_content = f"""你是一个文章总结助手，负责将文章内容整理成：一句话总结、重要要点、灵感与启发这三个部分内容
                请按照格式输出为排版美观的纯文本格式：

                # 一句话总结

                # 重要要点

                # 灵感与启发

                ：{content}
                """

                # 发送请求到OpenAI API，请求生成文章总结
                completion = client.chat.completions.create(
                    model="yi-medium-200k",
                    messages=[{"role": "user", "content": request_content}],
                    max_tokens=20000,
                    top_p=0.8,
                )

                # 获取生成的总结内容
                outputtext = completion.choices[0].message.content
                return outputtext

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # 运行异步函数并等待其完成
    return asyncio.run(download_and_transcribe())

if __name__ == "__main__":
    summary = get_bilibili_summary("https://www.bilibili.com/video/BV1gC41177xR/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=5531fb0981ef79f87198a3c2651dff93")
    if summary:
        print(summary)