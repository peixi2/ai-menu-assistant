# -*- coding: utf-8 -*-
# AI 核心逻辑：命令行版（waiter.py）和网页版（app.py）共用
import json
import os

from openai import OpenAI

from menu_data import search_menu

# 连接 DeepSeek（它的接口和 OpenAI 完全兼容，所以用 openai 这个包）
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# 告诉 AI：你有一个可以调用的工具，以及工具的参数格式
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_menu",
            "description": "在餐厅菜单里搜索菜品，可以按菜名关键词、类别、最高价格筛选",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "菜名关键词，例如：鱼、蛋糕、千层。没有就留空",
                    },
                    "category": {
                        "type": "string",
                        "description": "菜品类别，例如：肉类、海鲜类、蔬菜类、主食、甜食、饮料、水果。没有要求就留空",
                    },
                    "max_price": {
                        "type": "number",
                        "description": "能接受的最高价格（元）。没有限制就留空",
                    },
                },
            },
        },
    }
]

SYSTEM_PROMPT = (
    "你是这家餐厅的 AI 点餐助手，名叫小餐。"
    "顾客会问你菜单相关的问题。"
    "回答规则：\n"
    "1. 涉及菜品信息的问题（有什么菜、多少钱、推荐等），必须先调用 search_menu 工具查询，"
    "不要凭空编造菜品。\n"
    "2. 根据查询结果如实回答，推荐菜品时说明理由。\n"
    "3. 菜单数据库里没有辣度/口味字段。顾客问辣不辣时，可以凭菜名常识推断"
    "（如宫保鸡丁、辣椒炒肉通常偏辣），并说明这是根据菜名推断的。\n"
    "4. 回答用中文，语气亲切简短。"
)


def ask_ai(messages):
    """一轮对话：让 AI 回答问题。如果 AI 要调用工具，就执行工具再把结果喂回去。

    返回 (最终回答, 工具调用记录)。工具调用记录形如
    [{"name": "search_menu", "args": {"category": "主食"}}]，方便两个界面各自展示。
    """
    trace = []

    # 第一次请求：AI 决定是直接回答，还是调用工具
    resp = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=TOOLS,
    )
    msg = resp.choices[0].message
    messages.append(msg.model_dump())  # 把 AI 的回复记入历史

    # 如果 AI 想调用工具
    if msg.tool_calls:
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)  # AI 给出的参数
            trace.append({"name": call.function.name, "args": args})
            result = search_menu(**args)  # 真正执行工具
            # 把工具的执行结果告诉 AI
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )

        # 第二次请求：AI 拿到工具结果，组织出最终回答
        resp2 = client.chat.completions.create(model="deepseek-v4-flash", messages=messages)
        final = resp2.choices[0].message
        messages.append(final.model_dump())
        return final.content, trace

    return msg.content, trace
