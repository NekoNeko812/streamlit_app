import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("都道府県別道路の実延長と舗装済延長の推移")
st.write("test")

df = pd.read_csv("都道府県別道路の実延長と舗装済延長.csv", encoding="shift_jis")
selected_columns = ["都道府県"]

with st.sidebar:
  st.subheader("表示する都道府県")
  prefectures = st.multiselect("検索したい都道府県を選択してください（複数選択可）",
                          df["都道府県"].unique())
  want = st.multiselect("得たい情報を選択してください",
                            ["実延長", "舗装済延長", "舗装率"])

filtered_df = df[df["都道府県"].isin(prefectures)]

tab1, tab2, tab3 = st.tabs(["表", "指定年", "複数年"])

# 表のタブ
with tab1:
    st.header("表")

    with st.expander("得たい情報選択"):
          year = st.multiselect("年を指定してください",
                          list(range(2016, 2025)))


    st.write(year)
    st.write(want)

    for i in year:
        for j in want:
            col_name = f"{i}/{j}"
            if col_name in df.columns:
                selected_columns.append(col_name)

    if len(year) > 0 and len(want) > 0:
        display_df = filtered_df[selected_columns]
        st.write("単位：実延長・舗装済延長(km), 舗装率(%)")
        display_df.set_index("都道府県", inplace=True)
        st.dataframe(display_df)
    else:
        st.info("年と得たい情報を選択してください")
# 指定年のタブ
with tab2:
    st.header("指定年")
    
    with st.expander("得たい情報選択"):
          year = st.selectbox("年を指定してください",
                          range(2016, 2025))

    for j in want:
        col_name = f"{year}/{j}"
        if col_name in df.columns:
            selected_columns.append(col_name)

    if len(want) > 0:
        display_df = filtered_df[selected_columns]
        st.write("単位：実延長・舗装済延長(km), 舗装率(%)")
        
        value_cols = [c for c in selected_columns if c != "都道府県"]

        # 2. px.bar に直接リストを渡す
        fig = px.bar(
            display_df,
            x="都道府県",   # 横軸
            y=value_cols,   # 描画したい列名のリストをそのまま渡す
            barmode="group", # グループ棒グラフ
            title="年度別比較"
        )

        # 3. 凡例などの表示を整える（オプション）
        fig.update_layout(
            xaxis_title="都道府県",
            yaxis_title="値",
            legend_title="項目"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("年と得たい情報を選択してください")          
          

# 複数年のタブ
with tab3:
    st.header("複数年")