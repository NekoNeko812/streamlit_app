import streamlit as st
import pandas as pd

st.title("都道府県別道路の実延長と舗装済延長の推移")
st.write("test")
df = pd.read_csv("都道府県別道路の実延長と舗装済延長.csv", encoding="shift_jis")

with st.sidebar:
  st.subheader("表示する都道府県")
  prefectures = st.multiselect("検索したい都道府県を選択してください（複数選択可）",
                          df["都道府県"].unique())

tab1, tab2, tab3 = st.tabs(["表", "指定年", "複数年"])

with tab1:
    st.header("表")

    with st.expander("得たい情報選択"):
          year = st.multiselect("年を指定してください",
                          list(range(2016, 2025)))
          want = st.multiselect("得たい情報を選択してください",
                                ["実延長", "舗装済延長", "舗装率"])

    st.write(year)
    st.write(want)
    df = df[df["都道府県"].isin(prefectures)]
    # for i in year:
    #     df = df[df[f""]]

    st.write("単位：km")
    st.dataframe(df, width=800, height=220)

with tab2:
    st.write("指定年")

with tab3:
    st.write("複数年")