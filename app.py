# -*- coding: utf-8 -*-
# AI 点餐助手（网页版）
# 运行前先设置密钥:  $env:DEEPSEEK_API_KEY = "sk-你的key"
# 启动:  python app.py  →  浏览器打开 http://127.0.0.1:5000
import math
import os

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from ai_core import SYSTEM_PROMPT, ask_ai
from menu_data import create_user, find_user, get_foods_page, get_notices

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ai-menu-assistant-dev-key")

# 菜品图片存在项目自己的 static/img 里（从 Menu-实训 复制过来的），换电脑也能用
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "img")

# 每个浏览器一段 AI 对话历史（存在内存里，重启服务就清空）
SESSIONS = {}


@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    page_size = 12
    foods, total = get_foods_page(page, page_size)
    total_page = max(1, math.ceil(total / page_size))
    return render_template(
        "index.html",
        foods=foods,
        notices=get_notices(),
        page=page,
        total_page=total_page,
        total=total,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = find_user(username)
        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("index"))
        return render_template("login.html", error="用户名或密码错误", username=username)
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            return render_template("register.html", error="用户名和密码不能为空")
        if find_user(username):
            return render_template(
                "register.html", error="注册失败，用户名可能已存在"
            )
        create_user(username, password)
        return render_template("login.html", msg="注册成功，请登录")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/img/<path:filename>")
def dish_image(filename):
    """按文件名返回菜品图片（数据库里存的是 image/菜名.jpg 这种相对路径）。"""
    return send_from_directory(IMG_DIR, filename)


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
        answer, tool_calls, dishes = ask_ai(messages)
    except Exception as e:
        messages.pop()  # 失败的那句用户话移出历史
        return jsonify({"error": str(e)}), 500
    return jsonify({"answer": answer, "tool_calls": tool_calls, "dishes": dishes})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
