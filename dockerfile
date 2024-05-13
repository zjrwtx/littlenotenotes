# 使用官方 Python 运行时作为父镜像
FROM python:3.10-slim

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录内容复制到位于 /app 的容器中
COPY . /app

# 安装 requirements.txt 中指定的任何需要的程序包
RUN pip install --no-cache-dir -r requirements.txt

# 使端口 5000 可供此容器外的环境使用
EXPOSE 5000

# 定义环境变量
# ENV NAME World

# 在容器启动时运行 app.py
CMD ["python", "app.py"]