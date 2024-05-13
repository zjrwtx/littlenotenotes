from flask import Flask, request, send_file, Response, jsonify
import requests
from io import BytesIO
from functools import wraps
from flask_cors import CORS
import openai
import  json
from dotenv import load_dotenv
import os
from bilibiliapi import get_bilibili_summary
from webpageapi import get_summary
from youtubeapi import get_youtube_summary
from base64 import b64encode
app = Flask(__name__)

CORS(app)

# CORS(app, resources={r"/*": {"origins": ["http://localhost:5500"]}})
CORS(app, resources={r"/*": {"origins": "*"}})


# 在使用API密钥和基础URL之前加载.env文件
load_dotenv()

# 现在可以通过os.environ访问这些值
# 前后端认证调用apikey
SECRET_API_KEY =os.environ.get("SECRET_API_KEY") 


def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        # 从请求头中获取API密钥
        api_key = request.headers.get('X-API-KEY')
        
        # 检查API密钥是否正确
        if api_key and api_key == SECRET_API_KEY:
            # 如果API密钥正确，继续执行视图函数
            return view_function(*args, **kwargs)
        else:
            # 如果API密钥错误或缺失，返回错误信息
            return jsonify({"error": "Invalid or missing API key"}), 403

    return decorated_function


@app.route('/summary', methods=['POST'])
@require_apikey
def summary_api():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return {"error": "未提供URL。"}, 400
  
    elif original_url.startswith("https://www.bilibili.com/"):
        summary = get_bilibili_summary(original_url)
        if summary is None:
            return {"error": "生成笔记失败"}, 500
        return jsonify({"summary": summary})
    
    elif original_url.startswith("https://www.youtube.com/"):
        summary = get_youtube_summary(original_url)
        if summary is None:
            return {"error": "生成笔记失败"}, 500
        return jsonify({"summary": summary})

    else:
        summary = get_summary(original_url)
        if summary is None:
            return {"error": "生成笔记失败"}, 500
        return jsonify({"summary": summary})

  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



# curl请求例子

# curl -X POST \
#   http://yourserver.com/summary \
#   -H "Content-Type: application/json" \
#   -H "X-API-KEY: your-secret-api-key" \
#   -d '{"url": "http://example.com/page-to-summarize"}'