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
from menu_data import (
    add_food,
    add_notice,
    create_user,
    delete_food,
    delete_notice,
    find_user,
    get_all_foods,
    get_food,
    get_foods_page,
    get_notices,
    list_users,
    update_food,
    update_notice,
    update_user_role,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ai-menu-assistant-dev-key")

# 菜品图片存在项目自己的 static/img 里（从 Menu-实训 复制过来的），换电脑也能用
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "img")

# 每个浏览器一段 AI 对话历史（存在内存里，重启服务就清空）
SESSIONS = {}

# 不用登录就能访问的路径（和 Java 版 LoginFilter 一致：只有登录/注册放行）
FREE_PATHS = ("/login", "/register", "/static", "/img")


@app.before_request
def require_login():
    path = request.path
    if any(path == p or path.startswith(p + "/") for p in FREE_PATHS):
        return None
    if "user_id" not in session:
        if path in ("/chat", "/message"):
            return jsonify({"error": "请先登录"}), 401
        return redirect(url_for("login"))
    if path.startswith("/admin") and session.get("role") != 1:
        return redirect(url_for("index"))
    return None


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
            # 管理员进后台，普通用户进首页（和 Java 版一致）
            if user["role"] == 1:
                return redirect(url_for("admin_main"))
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
        # 用重定向而不是直接渲染：防止刷新页面时重复提交注册表单
        return redirect(url_for("login", registered=1, username=username))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- 管理员后台 ----------

@app.route("/admin")
def admin_main():
    return render_template(
        "admin/main.html",
        food_count=len(get_all_foods()),
        notice_count=len(get_notices()),
        user_count=len(list_users()),
    )


@app.route("/admin/foods")
def admin_foods():
    return render_template("admin/food_list.html", foods=get_all_foods())


def _food_form(food=None):
    images = sorted(os.listdir(IMG_DIR))
    return render_template("admin/food_form.html", food=food, images=images)


@app.route("/admin/foods/add", methods=["GET", "POST"])
def admin_food_add():
    if request.method == "POST":
        add_food(
            request.form["name"],
            request.form["image"],
            float(request.form["price"]),
            request.form["description"],
            int(request.form["status"]),
        )
        return redirect(url_for("admin_foods"))
    return _food_form()


@app.route("/admin/foods/edit/<int:food_id>", methods=["GET", "POST"])
def admin_food_edit(food_id):
    food = get_food(food_id)
    if food is None:
        return redirect(url_for("admin_foods"))
    if request.method == "POST":
        update_food(
            food_id,
            request.form["name"],
            request.form["image"],
            float(request.form["price"]),
            request.form["description"],
            int(request.form["status"]),
        )
        return redirect(url_for("admin_foods"))
    return _food_form(food)


@app.route("/admin/foods/delete/<int:food_id>", methods=["POST"])
def admin_food_delete(food_id):
    delete_food(food_id)
    return redirect(url_for("admin_foods"))


@app.route("/admin/notices")
def admin_notices():
    return render_template("admin/notice_list.html", notices=get_notices())


@app.route("/admin/notices/add", methods=["GET", "POST"])
def admin_notice_add():
    if request.method == "POST":
        add_notice(request.form["title"], request.form["content"])
        return redirect(url_for("admin_notices"))
    return render_template("admin/notice_form.html")


@app.route("/admin/notices/edit/<int:notice_id>", methods=["GET", "POST"])
def admin_notice_edit(notice_id):
    notices = [n for n in get_notices() if n["id"] == notice_id]
    if not notices:
        return redirect(url_for("admin_notices"))
    if request.method == "POST":
        update_notice(notice_id, request.form["title"], request.form["content"])
        return redirect(url_for("admin_notices"))
    return render_template("admin/notice_form.html", notice=notices[0])


@app.route("/admin/notices/delete/<int:notice_id>", methods=["POST"])
def admin_notice_delete(notice_id):
    delete_notice(notice_id)
    return redirect(url_for("admin_notices"))


@app.route("/admin/users")
def admin_users():
    return render_template("admin/user_list.html", users=list_users())


@app.route("/admin/users/role/<int:user_id>", methods=["POST"])
def admin_user_role(user_id):
    update_user_role(user_id, int(request.form["role"]))
    return redirect(url_for("admin_users"))


# ---------- 其他 ----------

@app.route("/message", methods=["POST"])
def message():
    """留言板：用户留言写入 notice 表，参与公告轮播，管理员在公告管理里管理。"""
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "留言不能为空"}), 400
    if len(content) > 200:
        return jsonify({"error": "留言最多 200 字"}), 400
    title = f"{session.get('username', '匿名')} 的留言"
    add_notice(title=title, content=content)
    return jsonify({"ok": True, "title": title, "content": content})


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
