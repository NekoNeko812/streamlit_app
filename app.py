import streamlit as st
import pandas as pd

st.title("都道府県別道路の実延長の推移")

df = pd.read_csv("都道府県別道路の実延長と舗装済延長.csv", encoding="shift_jis")

with st.sidebar:
  st.subheader("絞り込み条件")
  selected_cats = st.multiselect("都道府県を選択してください（複数選択可）",
                          df["都道府県"].unique())


