import pandas as pd
import streamlit as st
from utils import dataframe_agent

def create_chart(input_data, chart_type):
    #streamlit图表函数不支持列表，先转换为DataFrame
    df_data = pd.DataFrame(input_data["data"],
                           columns=input_data["columns"])
    #图表绘制前还需要设置DataFrame索引,索引会被用来表示图表的横轴
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

st.header("💡 数据分析智能工具")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://api.aigc369.com/register?aff=87kh)")

data = st.file_uploader("上传你的数据文件（CSV格式）：", type="csv")
if data:
    st.session_state["df"] = pd.read_csv(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

question = st.text_area("请输入关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")
button = st.button("生成回答")

if button:
    if not openai_api_key:
        st.info("请输入你的OpenAI API密钥")
        st.stop()

    if "df" not in st.session_state:
        st.info("请上传你的数据文件")
        st.stop()

    with st.spinner("AI正在思考中，请稍等..."):
        result_dict = dataframe_agent(st.session_state["df"], question, openai_api_key)
        if "answer" in result_dict:
            st.write(result_dict["answer"])
        if "table" in result_dict:
            st.table(pd.DataFrame(result_dict["table"]["data"],
                                  columns=result_dict["table"]["columns"]))
        if "bar" in result_dict:
            create_chart(result_dict["bar"], "bar")
        if "line" in result_dict:
            create_chart(result_dict["line"], "line")
        if "scatter" in result_dict:
            create_chart(result_dict["scatter"], "scatter")