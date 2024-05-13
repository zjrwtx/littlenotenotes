# 使用官方 Python 运行时作为父镜像
FROM python:3.10-slim

# 更新软件包列表并安装FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录内容复制到位于 /app 的容器中
COPY . /app

# 安装 requirements.txt 中指定的任何需要的程序包
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install  -r requirements.txt

# 使端口 5000 可供此容器外的环境使用
EXPOSE 8080


# 定义环境变量
# ENV NAME World

# 在容器启动时运行 app.py
CMD ["python", "main.py"]