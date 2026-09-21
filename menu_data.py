# -*- coding: utf-8 -*-
# 第三步：从模拟数据换成查真实 MySQL（menu_system 库，就是你 Menu-实训 项目用的那个）
import os

import pymysql

# 连接信息默认和 Menu-实训 的 c3p0-config.xml 保持一致，
# 别人的电脑可以通过环境变量 DB_HOST / DB_USER / DB_PASSWORD 等覆盖（见 README）
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "123456"),
    "database": os.environ.get("DB_NAME", "menu_system"),
    "charset": "utf8mb4",
}


def _query(sql, params=None):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()


def search_menu(keyword: str = None, category: str = None, max_price: float = None):
    """按条件查真实菜单。这就是 AI 可以调用的“工具函数”。"""
    sql = "SELECT name, description, price, image FROM food WHERE status = 1"
    conds, params = [], []
    if keyword:
        conds.append("name LIKE %s")
        params.append(f"%{keyword}%")
    if category:
        conds.append("description LIKE %s")
        params.append(f"%{category}%")
    if max_price is not None:
        conds.append("price <= %s")
        params.append(max_price)
    if conds:
        sql += " AND " + " AND ".join(conds)
    sql += " ORDER BY price"

    rows = _query(sql, params)
    # 真实表里类别存在 description 字段，price 是 Decimal，转成 float 方便 AI 读
    return [
        {
            "name": r["name"],
            "category": r["description"],
            "price": float(r["price"]),
            "image": r["image"],
        }
        for r in rows
    ]


def get_foods_page(page=1, page_size=12):
    """首页菜品展示用：分页查上架菜品。返回 (菜品列表, 总数)。"""
    total = _query("SELECT COUNT(*) AS c FROM food WHERE status = 1")[0]["c"]
    offset = (page - 1) * page_size
    rows = _query(
        "SELECT name, description, price, image FROM food WHERE status = 1"
        " ORDER BY id LIMIT %s, %s",
        (offset, page_size),
    )
    foods = [
        {
            "name": r["name"],
            "category": r["description"],
            "price": float(r["price"]),
            "image": r["image"],
        }
        for r in rows
    ]
    return foods, total


def get_notices():
    """公告轮播：全部公告按时间倒序。"""
    return _query("SELECT title, content FROM notice ORDER BY create_time DESC")


def find_user(username):
    """登录用：按用户名查用户。"""
    rows = _query(
        "SELECT id, username, password, role FROM user WHERE username = %s",
        (username,),
    )
    return rows[0] if rows else None


def create_user(username, password):
    """注册：新增普通用户（role=2），和 Java 版逻辑一致。"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user(username, password, role) VALUES(%s, %s, 2)",
                (username, password),
            )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    # 自己先试试这个函数能不能用
    print("全部上架菜品数量：", len(search_menu()))
    print("搜索“鸡”：", search_menu(keyword="鸡"))
    print("甜食类：", search_menu(category="甜食"))
    print("10 元以内：", search_menu(max_price=10))
