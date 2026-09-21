# -*- coding: utf-8 -*-
# AI 点餐助手（命令行版）—— AI 逻辑在 ai_core.py，网页版见 app.py
# 运行前先安装依赖:  pip install openai pymysql
# 运行前先设置密钥:  $env:DEEPSEEK_API_KEY = "sk-你的key"
from ai_core import SYSTEM_PROMPT, ask_ai


def main():
    print("=" * 40)
    print(" 欢迎光临！我是 AI 点餐助手「小餐」")
    print(" 试试问我：有什么主食？ / 10 块钱能吃什么？ / 有没有辣的菜？")
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
            answer, tool_calls, _ = ask_ai(messages)  # 第三个返回值是查到的菜品，命令行版用不上
            for call in tool_calls:
                print(f"   [工具调用] {call['name']}({call['args']})")
            print(f"\n小餐: {answer}")
        except Exception as e:
            print(f"\n出错了: {e}")
            messages.pop()  # 把刚才失败的那句用户话移出历史


if __name__ == "__main__":
    main()
