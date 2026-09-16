# -*- coding: utf-8 -*-
# 第三步：从模拟数据换成查真实 MySQL（menu_system 库，就是你 Menu-实训 项目用的那个）
import pymysql

# 连接信息和 Menu-实训 的 c3p0-config.xml 保持一致
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "menu_system",
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
    sql = "SELECT name, description, price FROM food WHERE status = 1"
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
        {"name": r["name"], "category": r["description"], "price": float(r["price"])}
        for r in rows
    ]


if __name__ == "__main__":
    # 自己先试试这个函数能不能用
    print("全部上架菜品数量：", len(search_menu()))
    print("搜索“鸡”：", search_menu(keyword="鸡"))
    print("甜食类：", search_menu(category="甜食"))
    print("10 元以内：", search_menu(max_price=10))
