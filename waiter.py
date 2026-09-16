# -*- coding: utf-8 -*-
# AI 点餐助手（命令行版）
# 运行前先安装依赖:  pip install openai
# 运行前先设置密钥:  $env:DEEPSEEK_API_KEY = "sk-你的key"
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
            "description": "在餐厅菜单里搜索菜品，可以按菜名关键词、口味、最高价格筛选",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "菜名关键词，例如：鱼、蛋糕、千层。没有就留空",
                    },
                    "taste": {
                        "type": "string",
                        "description": "口味，可选值：辣、不辣、甜。没有要求就留空",
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
    "3. 回答用中文，语气亲切简短。"
)


def ask_ai(messages):
    """一轮对话：让 AI 回答问题，如果 AI 要调用工具，就执行工具再把结果喂回去"""
    # 第一次请求：AI 决定是直接回答，还是调用工具
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOLS,
    )
    msg = resp.choices[0].message
    messages.append(msg.model_dump())  # 把 AI 的回复记入历史

    # 如果 AI 想调用工具
    if msg.tool_calls:
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)  # AI 给出的参数
            print(f"   [工具调用] search_menu({args})")
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
        resp2 = client.chat.completions.create(model="deepseek-chat", messages=messages)
        final = resp2.choices[0].message
        messages.append(final.model_dump())
        return final.content

    return msg.content


def main():
    print("=" * 40)
    print(" 欢迎光临！我是 AI 点餐助手「小餐」")
    print(" 试试问我：有什么不辣的菜？ / 推荐几个甜点")
    print(" 输入 exit 退出")
    print("=" * 40)

    # messages 是整段对话的记录，每次对话都带着历史，AI 才有“记忆”
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ("exit", "quit", "退出"):
            print("再见！")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        try:
            answer = ask_ai(messages)
            print(f"\n小餐: {answer}")
        except Exception as e:
            print(f"\n出错了: {e}")
            messages.pop()  # 把刚才失败的那句用户话移出历史


if __name__ == "__main__":
    main()
