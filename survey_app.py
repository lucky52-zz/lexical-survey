import streamlit as st
import pandas as pd

# --- 1. 初始化和设置 ---

# 设置页面
st.set_page_config(page_title="词汇熟悉度评定", page_icon="📝")

# 预测试的词汇列表
word_list = [
    'forgot', 'blew', 'shook', 'dealt', 'kept', 'sent', 'write', 'freeze', 'spoke', 'lay', 
    'heard', 'understood', 'fight', 'drank', 'steal', 'built', 'chose', 'bring', 'wore', 
    'swam', 'lost', 'forbade', 'teach', 'threw', 'leave', 'sold', 'took', 'overcame', 
    'flew', 'know', 'swore', 'found', 'hung', 'held', 'rode', 'speak', 'spun', 'grow', 
    'sang', 'rang', 'struck', 'sleep', 'find', 'give', 'forgive', 'left', 'bought', 
    'spend', 'bend', 'paid', 'came', 'swim', 'began', 'told', 'swept', 'drive', 'hear', 
    'spun', 'feel', 'wore', 'made', 'fought', 'run', 'taught', 'threw', 'stick', 'broke', 
    'choose', 'understood', 'felt', 'shoot', 'knew', 'grew', 'thought', 'drew', 'gave', 
    'said', 'took', 'tear', 'catch', 'forget', 'became', 'paid', 'spilt', 'bent', 'kept', 
    'come', 'tell', 'buy', 'caught', 'began', 'mistake', 'dealt', 'blew', 'drank', 
    'became', 'build', 'drive', 'learn', 'made', 'shake', 'sank', 'see', 'ring', 
    'sell', 'mean', 'rode', 'lent', 'ran', 'lose', 'meant', 'pay', 'sent', 'sank', 
    'shoot', 'learnt', 'sang', 'saw', 'mistook', 'sat', 'sing', 'break', 'bring', 'sit', 
    'spilt', 'shook', 'slid', 'spent', 'wake', 'think', 'slide', 'sweep', 'tore', 'woke', 
    'wrote', 'lay', 'leave', 'spin', 'say', 'lend', 'stick', 'freeze', 'hold', 'hang', 
    'steal', 'ride', 'understand', 'wear', 'overcome', 'seek', 'swing', 'teach', 
    'stand', 'sought', 'stood', 'swung', 'sink', 'forgive', 'feed', 'send'
]

# 初始化Session State
if 'page' not in st.session_state:
    st.session_state.page = 'instructions'
if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0
if 'results' not in st.session_state:
    st.session_state.results = []
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')

# --- 2. 定义页面函数 ---

def show_instructions_page():
    st.title("英语词汇熟悉度评定")
    st.markdown("""
    您好！
    感谢您参与本次预测试。我们正在为一项正式的心理语言学实验筛选合适的词汇，您的反馈至关重要。

    **任务说明：**
    接下来，您将看到一系列英语单词，它们会逐一呈现在屏幕上。您的任务是，根据您的第一感觉，**快速评定您对每一个单词的熟悉程度**。

    **评定标准：**
    请使用 **1-7** 的评分标准，其中：
    - **1 = 完全不认识** (我从未见过这个词)
    - **4 = 好像见过** (有些印象，但不确定意思，需要仔细想)
    - **7 = 极其熟悉** (像 `apple`, `book`, `water` 一样熟悉，瞬间就能反应出意思)

    **重要提示：**
    - 请**完全依赖您的第一直觉**进行快速判断，不要在任何一个词上停留过久。
    - 这**没有对错之分**，我们只关心您最真实的个人感受。
    - 整个过程大约需要5-8分钟。

    再次感谢您的宝贵时间和帮助！
    """)
    if st.button("我已了解，开始测试", type="primary"):
        st.session_state.page = 'survey'
        st.rerun()

def show_survey_page():
    word_index = st.session_state.current_word_index
    if word_index >= len(word_list):
        st.session_state.page = 'thank_you'
        st.rerun()
    
    current_word = word_list[word_index]

    st.title("请评定以下单词的熟悉度")
    progress = (word_index + 1) / len(word_list)
    st.progress(progress, text=f"进度: {word_index + 1} / {len(word_list)}")

    st.markdown(f"<h1 style='text-align: center; color: blue;'>{current_word}</h1>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("请选择您的熟悉度评分 (1 = 完全不认识, 7 = 极其熟悉):")

    cols = st.columns(7)
    ratings = [1, 2, 3, 4, 5, 6, 7]
    for i, col in enumerate(cols):
        with col:
            if st.button(str(ratings[i]), key=f"rate_{ratings[i]}", use_container_width=True):
                st.session_state.results.append({'word': current_word, 'rating': ratings[i]})
                st.session_state.current_word_index += 1
                st.rerun()

def show_thank_you_page():
    st.balloons()
    st.success("🎉 您已完成所有评定！非常感谢您的参与！")
    
    # 将本次结果转换为DataFrame
    results_df = pd.DataFrame(st.session_state.results)
    
    # ------------------- 核心修改在这里 -------------------
    # 将DataFrame转换为CSV格式的字符串，以供下载
    # .encode('utf-8-sig') 是为了确保Excel能正确打开，避免中文乱码
    csv_data = results_df.to_csv(index=False).encode('utf-8-sig')

    st.info("请点击下方的按钮下载您的答题结果，并将文件发送给研究者。")

    # 创建下载按钮
    st.download_button(
        label="✅ 下载您的答题结果 (CSV文件)",
        data=csv_data,
        file_name=f"results_{st.session_state.participant_id}.csv",
        mime="text/csv",
    )
    # ----------------------------------------------------
    
    st.write("---")
    st.write("以下是您本次提交的数据预览：")
    st.dataframe(results_df)

# --- 3. 主程序逻辑 ---

if st.session_state.page == 'instructions':
    show_instructions_page()
elif st.session_state.page == 'survey':
    show_survey_page()
elif st.session_state.page == 'thank_you':
    show_thank_you_page()
