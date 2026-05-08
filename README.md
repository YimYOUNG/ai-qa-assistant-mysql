# AI 问答助手 

基于大模型 API 的智能问答系统，支持 MySQL 数据持久化、热门话题统计分析。

## 功能特点

- 🤖 调用智谱AI大模型 API 进行智能问答
- 💾 MySQL 数据库持久化，每次问答自动保存
- 📊 热门话题统计：最近7天提问最多的 TOP 5
- 🎨 Streamlit Web 界面，开箱即用
- 🔐 配置与代码分离，敏感信息不提交

## 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.9+ | 主编程语言 |
| Streamlit | Web 界面框架 |
| MySQL + PyMySQL | 数据库存储 |
| 智谱AI API | 大模型调用 |

## 项目结构
my_ai_qi_tool/
├── app.py # 主程序
├── requirements.txt # 依赖包列表
├── .gitignore # Git 忽略文件
└── README.md # 项目说明

## 快速开始

### 1. 安装依赖


pip install -r requirements.txt

#### 2. 配置 MySQL
在 MySQL 中创建数据库：

CREATE DATABASE ai_qa_db;

#### 3. 配置 API Key 和数据库密码
创建 config.py 文件：

python
API_KEY = "你的智谱API Key"

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '你的MySQL密码',
    'database': 'ai_qa_db',
    'charset': 'utf8mb4'
}

##### 4. 运行项目
streamlit run app.py

浏览器会自动打开 http://localhost:8501