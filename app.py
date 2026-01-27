import streamlit as st
import pandas as pd

st.title("都道府県別道路の実延長と舗装済延長の推移")
st.write("test")

df = pd.read_csv("都道府県別道路の実延長と舗装済延長.csv", encoding="shift_jis")
with st.sidebar:
  st.subheader("表示する都道府県")
  prefectures = st.multiselect("検索したい都道府県を選択してください（複数選択可）",
                          df["都道府県"].unique())

filtered_df = df[df["都道府県"].isin(prefectures)]

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

    selected_colmns = ["都道府県"]
    for i in year:
        for j in want:
            col_name = f"{i}/{j}"
            if col_name in df.columns:
                selected_colmns.append(col_name)

    if len(year) > 0 and len(want) > 0:
        display_df = filtered_df[selected_colmns]
        st.write("単位：km")
        display_df.set_index("都道府県", inplace=True)
        st.dataframe(display_df)
    else:
        st.info("年と得たい情報を選択してください")

with tab2:
    st.write("指定年")

with tab3:
    st.write("複数年")