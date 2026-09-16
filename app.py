# -*- coding: utf-8 -*-
# AI 点餐助手（网页版）
# 运行前先设置密钥:  $env:DEEPSEEK_API_KEY = "sk-你的key"
# 启动:  python app.py  →  浏览器打开 http://127.0.0.1:5000
from flask import Flask, jsonify, render_template, request

from ai_core import SYSTEM_PROMPT, ask_ai

app = Flask(__name__)

# 每个浏览器页面一段对话历史（存在内存里，重启服务就清空）
SESSIONS = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    sid = str(data.get("session_id", "default"))
    user_text = (data.get("message") or "").strip()
    if not user_text:
        return jsonify({"error": "消息不能为空"}), 400

    messages = SESSIONS.setdefault(sid, [{"role": "system", "content": SYSTEM_PROMPT}])
    messages.append({"role": "user", "content": user_text})
    try:
        answer, tool_calls = ask_ai(messages)
    except Exception as e:
        messages.pop()  # 失败的那句用户话移出历史
        return jsonify({"error": str(e)}), 500
    return jsonify({"answer": answer, "tool_calls": tool_calls})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
