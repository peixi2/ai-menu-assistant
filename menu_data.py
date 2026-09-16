# -*- coding: utf-8 -*-
# 第一步先用模拟数据（菜名沿用你 Menu 实训项目的真实菜品）
# 第三步会把这个文件换成查真实 MySQL 数据库

MENU = [
    {"name": "宫保鸡丁",   "category": "热菜", "taste": "辣",   "price": 28},
    {"name": "麻婆豆腐",   "category": "热菜", "taste": "辣",   "price": 18},
    {"name": "辣椒炒肉",   "category": "热菜", "taste": "辣",   "price": 26},
    {"name": "清蒸鱼",     "category": "热菜", "taste": "不辣", "price": 48},
    {"name": "番茄炒蛋",   "category": "热菜", "taste": "不辣", "price": 16},
    {"name": "蒜蓉空心菜", "category": "热菜", "taste": "不辣", "price": 14},
    {"name": "白切鸡",     "category": "热菜", "taste": "不辣", "price": 38},
    {"name": "煲仔饭",     "category": "主食", "taste": "不辣", "price": 22},
    {"name": "云吞面",     "category": "主食", "taste": "不辣", "price": 15},
    {"name": "法棍",       "category": "主食", "taste": "不辣", "price": 12},
    {"name": "双皮奶",     "category": "甜品", "taste": "甜",   "price": 10},
    {"name": "芒果千层",   "category": "甜品", "taste": "甜",   "price": 20},
    {"name": "巧克力蛋糕", "category": "甜品", "taste": "甜",   "price": 18},
    {"name": "草莓舒芙蕾", "category": "甜品", "taste": "甜",   "price": 22},
    {"name": "树莓冰淇淋", "category": "甜品", "taste": "甜",   "price": 12},
    {"name": "西瓜汁",     "category": "饮品", "taste": "甜",   "price": 8},
    {"name": "橙汁",       "category": "饮品", "taste": "甜",   "price": 8},
    {"name": "冰香草拿铁", "category": "饮品", "taste": "甜",   "price": 16},
    {"name": "矿泉水",     "category": "饮品", "taste": "不辣", "price": 3},
]


def search_menu(keyword: str = None, taste: str = None, max_price: float = None):
    """按条件筛选菜品。这就是将来 AI 可以调用的“工具函数”。"""
    results = MENU
    if keyword:
        results = [d for d in results if keyword in d["name"]]
    if taste:
        results = [d for d in results if taste in d["taste"]]
    if max_price is not None:
        results = [d for d in results if d["price"] <= max_price]
    return results


if __name__ == "__main__":
    # 自己先试试这个函数能不能用
    print(search_menu(keyword="千层"))
