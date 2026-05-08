import streamlit as st
import requests
import pymysql
from datetime import datetime
from config import API_KEY, DB_CONFIG   # 从 config.py 读取配置

# ---------- 1. 获取数据库连接 ----------
def get_conn():
    return pymysql.connect(**DB_CONFIG)

# ---------- 2. 初始化表 ----------
def ensure_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_records (
            id INT PRIMARY KEY AUTO_INCREMENT,
            question TEXT,
            answer TEXT,
            model VARCHAR(50),
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# ---------- 3. 保存问答记录 ----------
def save_record(question, answer, model):
    conn = get_conn()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO qa_records (question, answer, model, timestamp) VALUES (%s, %s, %s, %s)",
        (question, answer, model, now)
    )
    conn.commit()
    conn.close()

# ---------- 4. 查询统计 ----------
def get_top_questions(limit=5):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT question, COUNT(*) as cnt
        FROM qa_records
        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY question
        ORDER BY cnt DESC
        LIMIT %s
    ''', (limit,))
    results = cursor.fetchall()
    conn.close()
    return results

# ---------- 5. 页面配置 ----------
st.set_page_config(page_title="QAQ我的智能问答助手")
st.title("我的智能问答助手")

# 确保表存在
ensure_table()

# 侧边栏
with st.sidebar:
    # API Key 现在从 config.py 读取
    st.success("API Key 已配置")
    
    st.divider()
    st.subheader(" 数据统计")
    
    top_questions = get_top_questions(5)
    if top_questions:
        st.write("**最近7天热门问题 TOP 5**")
        for i, (q, c) in enumerate(top_questions, 1):
            st.write(f"{i}. [{c}次] {q[:30]}...")
    else:
        st.write("暂无数据，先问几个问题吧")

# 主界面
user_question = st.chat_input("问我点什么吧...")

if user_question:
    with st.chat_message("user"):
        st.write(user_question)
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "glm-4-flash",
                "messages": [{"role": "user", "content": user_question}]
            }
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                result = response.json()
                answer = result['choices'][0]['message']['content']
                st.write(answer)
                
                # 保存到 MySQL
                save_record(user_question, answer, "glm-4-flash")
                
            except Exception as e:
                st.error(f"调用失败: {e}")