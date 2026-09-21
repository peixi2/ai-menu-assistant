# AI 点餐助手「小餐」

一个用来学习 **Function Calling（函数调用）** 的 AI 点餐助手项目：接 DeepSeek 大模型 + 真实 MySQL 菜单库，让 AI 自己决定什么时候查菜单、用什么条件查，再根据查询结果回答顾客。

提供两种界面：

- **网页版**：完整餐厅网站——首页菜品展示（搜索/分页）+ 公告轮播 + 登录注册，右下角悬浮 AI 聊天窗随时可问，AI 查到菜后展示图片卡片
- **命令行版**：终端里直接聊

## 核心原理：Function Calling

```
顾客提问 ──→ AI 判断需要查菜单 ──→ 调用 search_menu(关键词/类别/价格)
   ↑                                        │
最终回答 ←── AI 根据真实结果组织语言 ←── 把查询结果回填给 AI
```

整个过程是一个多轮循环：每一轮请求都带上 tools 参数，AI 想查就真正执行工具、把结果喂回去，直到它给出最终回答（核心代码在 `ai_core.py` 的 `ask_ai`）。

## 功能

- **登录门禁**：未登录只能访问登录/注册页，其他页面自动跳转登录（和 Java 版 LoginFilter 一致）
- 首页菜品展示：卡片网格（图/名/价/描述），前端全局模糊搜索（按字匹配菜名+类别，全部菜品都能搜到、不受分页限制）+ 分页（每页 12 条）
- 公告轮播：读 notice 表，6 秒自动切换
- 留言板：公告区左下角按钮，登录用户可写留言（最多 200 字），留言进入公告轮播，管理员在后台公告管理里可删除
- 登录 / 注册 / 退出：和 Menu-实训 Java 项目共用同一张 user 表；管理员登录进后台，普通用户进首页
- **后台管理**（管理员）：菜品增删改、公告增删改、用户列表 + 修改角色
- AI 悬浮聊天窗：任何页面右下角点开即聊，按菜名关键词 / 类别 / 最高价格查菜单，推荐菜品并说明理由
- AI 查到菜后展示图片卡片（图片失败自动隐藏）
- 同一浏览器内对话有记忆（localStorage 存会话 id）

## 快速开始

### 1. 环境要求

- Python 3.10+
- MySQL 8（本地装一个即可）

### 2. 安装依赖

```powershell
pip install -r requirements.txt
```

> Windows 用户也可以跳过这一步：直接双击项目里的 `start.bat`，会自动创建虚拟环境、安装依赖并启动网页版（数据库和 API Key 仍需按下面步骤准备）。

### 3. 准备数据库

先建库，再导入表结构和数据（`sql/food.sql` 包含 food 菜品表 + 51 道菜、notice 公告表、user 用户表结构）：

```powershell
mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS menu_system DEFAULT CHARSET utf8mb4;"
mysql -uroot -p menu_system < sql/food.sql
```

> 脚本里的 user 表带一个演示管理员：`admin` / `admin123`。普通账号请用注册页注册，想体验后台管理就用管理员登录。

如果 MySQL 的用户名/密码不是 `root/123456`，用环境变量覆盖：

```powershell
$env:DB_USER = "你的用户名"
$env:DB_PASSWORD = "你的密码"
```

支持的环境变量：`DB_HOST`、`DB_PORT`、`DB_USER`、`DB_PASSWORD`、`DB_NAME`。

### 4. 申请 DeepSeek API Key

1. 打开 https://platform.deepseek.com 注册并充值一点余额
2. 创建 API Key 并复制
3. 在当前终端设置环境变量：

```powershell
$env:DEEPSEEK_API_KEY = "sk-你的key"
```

> key 只在终端里设置，**千万别写进代码或提交到 GitHub**（本项目已把 `.env` 加进 .gitignore）。

### 5. 启动

网页版：

```powershell
python app.py
# 浏览器打开 http://127.0.0.1:5000
```

命令行版：

```powershell
python waiter.py
```

试试问它：「有什么主食？」「10 块钱能吃什么？」「推荐点甜食」。

## 文件结构

| 文件 | 作用 |
|------|------|
| `ai_core.py` | AI 核心逻辑：工具声明、多轮工具调用循环（命令行和网页共用） |
| `menu_data.py` | 数据库层：`search_menu` 工具函数 + 分页查菜品 + 公告 + 用户 + 后台增删改 |
| `waiter.py` | 命令行版入口 |
| `app.py` | Flask 网页版入口（端口 5000）：登录拦截、首页、登录注册、后台管理、聊天 API、图片路由 |
| `templates/base.html` | 公共布局：顶部导航 + 悬浮 AI 聊天窗（所有页面共用） |
| `templates/index.html` | 首页：公告轮播 + 菜品展示 + 搜索 + 分页 |
| `templates/login.html` `templates/register.html` | 登录 / 注册页 |
| `templates/admin/` | 后台管理页面：主页、菜品管理、公告管理、用户管理 |
| `static/img/` | 菜品图片（51 张） |
| `sql/food.sql` | 表结构 + 菜品/公告数据 + 演示管理员账号 |

## 已知限制

- 对话历史存在内存里，重启服务就清空
- AI 模型名在 `ai_core.py` 里写的是 `deepseek-v4-flash`，可按需修改
- 用户密码为明文存储（与 Menu-实训 Java 项目共用 user 表、保持一致；真实项目应改为哈希存储）
