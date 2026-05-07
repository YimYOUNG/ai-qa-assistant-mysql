import streamlit as st
import requests

# 页面标题
st.set_page_config(page_title="我的智能问答助手")
st.title("🤖 我的智能问答助手")

# 侧边栏：用户输入API Key（出于安全考虑，不写在代码里）
with st.sidebar:
    api_key = st.text_input("请输入你的 API Key", type="password")
    st.markdown("[获取智谱AI免费API Key](https://open.bigmodel.cn/)")

# 主界面：用户问题和历史记录
user_question = st.chat_input("问我点什么吧...")

if user_question:
    if not api_key:
        st.error("请先在左侧输入你的API Key")
        st.stop()
    
    # 显示用户问题
    with st.chat_message("user"):
        st.write(user_question)
    
    # 调用大模型API
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "model": "glm-4-flash",
                "messages": [{"role": "user", "content": user_question}]
            }
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                result = response.json()
                answer = result['choices'][0]['message']['content']
                st.write(answer)
            except Exception as e:
                st.error(f"调用失败: {e}")