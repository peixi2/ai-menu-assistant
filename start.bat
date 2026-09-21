@echo off
chcp 65001 >nul
cd /d %~dp0
echo ==============================================
echo   AI 点餐助手「小餐」一键启动
echo ==============================================
echo.

if "%DEEPSEEK_API_KEY%"=="" (
    echo [提示] 未检测到 DEEPSEEK_API_KEY 环境变量，AI 聊天功能将不可用。
    echo        可以先关闭本窗口，在终端里设置后重新双击：
    echo        set DEEPSEEK_API_KEY=sk-你的key
    echo.
)

if not exist .venv (
    echo [1/2] 正在创建虚拟环境 .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo 创建失败：请确认已安装 Python 3.10+ 并加入 PATH
        pause
        exit /b 1
    )
) else (
    echo [1/2] 虚拟环境 .venv 已存在，跳过创建
)

call .venv\Scripts\activate.bat
echo [2/2] 安装依赖（requirements.txt）...
python -m pip install -r requirements.txt -q
echo.
echo 启动网页版：浏览器打开 http://127.0.0.1:5000
echo 按 Ctrl+C 停止服务
echo.
python app.py
pause
