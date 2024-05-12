from flask import Flask, request, send_file, Response, jsonify
import requests
from io import BytesIO
from functools import wraps
from flask_cors import CORS
import openai
import  json
from dotenv import load_dotenv
import os

from base64 import b64encode
app = Flask(__name__)

CORS(app)

# CORS(app, resources={r"/*": {"origins": ["http://localhost:5500"]}})
CORS(app, resources={r"/*": {"origins": "*"}})


# 在使用API密钥和基础URL之前加载.env文件
load_dotenv()

# 现在可以通过os.environ访问这些值

API_BASE = "https://api.lingyiwanwu.com/v1"
API_KEY = "a6022274cd8b44f182c5166cc4cc48bc"
# API_BASE = os.environ.get("API_BASE")
# API_KEY = os.environ.get("API_KEY")
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

@app.route('/summary', methods=['POST'])
@require_apikey
def summary_api():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return {"error": "未提供URL。"}, 400

    summary = get_summary(original_url)
    if summary is None:
        return {"error": "生成摘要失败"}, 500

    
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)



# curl请求例子

# curl -X POST \
#   http://yourserver.com/summary \
#   -H "Content-Type: application/json" \
#   -H "X-API-KEY: your-secret-api-key" \
#   -d '{"url": "http://example.com/page-to-summarize"}'