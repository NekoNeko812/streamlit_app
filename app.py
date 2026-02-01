import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")       # 横幅をブラウザに合わせる
colors = px.colors.qualitative.Plotly

st.title("都道府県別道路の実延長及び舗装状況の推移")
st.write("test")

df = pd.read_csv("都道府県別道路の実延長と舗装済延長.csv", encoding="shift_jis")

with st.sidebar:
  st.subheader("表示する情報")
  prefectures = st.multiselect("検索したい都道府県を選択してください（複数選択可）",
                          df["都道府県"].unique())
  st.text("得たい情報")
  want = st.multiselect("得たい情報を選択してください",
                            ["実延長", "舗装済延長"])
  per = st.checkbox("舗装率は表示しますか？", value=False)      # 元から選択されていない

filtered = df[df["都道府県"].isin(prefectures)]

tab1, tab2, tab3 = st.tabs(["表", "指定年", "複数年"])

# 表のタブ
with tab1:
    st.header("表")
    selected_columns_df = ["都道府県"]

    with st.expander("年"):
          year_df = st.multiselect("表で表示する年を指定してください",
                          list(range(2016, 2025)))


    # st.write(year_df)
    # st.write(want)

    for i in year_df:
        for j in want:
            selected_columns_df.append(f"{i}/{j}")
        if per == True:
            selected_columns_df.append(f"{i}/舗装率")



    if len(prefectures)>0 and len(year_df) > 0 and (len(want) > 0 or per == True):
        display = filtered[selected_columns_df]
        st.write("単位：km")
        display.set_index("都道府県", inplace=True)
        st.dataframe(display)
    else:
        st.info("都道府県と年と得たい情報を選択してください")

# 指定年のタブ
with tab2:
    st.header("指定年")
    selected_columns_bar = ["都道府県"]
    with st.expander("年"):
          year_bar = st.selectbox("棒グラフで表示する年を指定してください",
                          range(2016, 2025))
    
    # st.write(year_bar)
    # st.write(want)


    if len(prefectures)>0 and (len(want) > 0 or per == True):
        for j in want:
            selected_columns_bar.append(f"{year_bar}/{j}")
            
        if per == True:
            selected_columns_bar.append(f"{year_bar}/舗装率")
        display = filtered[selected_columns_bar]

        

        fig_bar = go.Figure() # 土台
        if per != True or (len(want) == 0 and per == True): # y軸が２ついらない場合
            value_cols_bar = [c for c in selected_columns_bar if c != "都道府県"]
        #選択された項目ごとに「棒の情報」を一つずつ足していくコード
            for col in value_cols_bar:
                fig_bar.add_trace(go.Bar(
                    x=display["都道府県"],
                    y=display[col],
                    name=col.split("/")[-1],
                    text=display[col],
                    textposition="auto"
                ))
        else:                       # y軸が２つ必要な場合
            colmuns_perin=[]        # 舗装率用リスト
            for i in want:
                colmuns_perin.append(f"{year_bar}/{i}")
            for col in colmuns_perin:           # 舗装率以外の棒              
                fig_bar.add_trace(go.Bar(
                x=display["都道府県"],
                y=display[col],
                name=col.split("/")[-1],
                text=display[col],
                textposition="auto",
                yaxis="y1",
                ))

            fig_bar.add_trace(go.Scatter(           # 舗装率の棒
                x=display["都道府県"],
                y=display[f"{year_bar}/舗装率"],
                name="舗装率",
                yaxis="y2",
                mode="markers",
                marker=dict(
                    color="orange",
                    size=10,
                    line=dict(
                        width=1,
                        color="white")
                ),
            ))
        # レイアウト設定
        if per==True and len(want)==0:      # 舗装率だけの時
            fig_bar.update_layout(
                yaxis=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 75] # 率は0-75に固定
                        ))
        else:                               # 舗装率以外もあるとき
            fig_bar.update_layout(
            yaxis=dict(
                title="延長",
                side="left"
                ),
            yaxis2=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 75] # 率は0-75に固定
                        ),
            )            
        fig_bar.update_layout(              # 基本設定
            barmode="group",
            title=f"{year_bar}年 道路状況比較",
            xaxis_title="都道府県",
            legend=dict(
                title_text="凡例",  
                orientation="h",    # 凡例を横並びにする
                yanchor="bottom",   # 凡例の下を起点にする
                y=1.1,              # グラフの上側
                xanchor="center",   # 凡例の中央を起点にする
                x=0.5,              # グラフの真ん中
            ),
            uniformtext_mode='hide',       # 小さすぎる数値テキストを隠す
            uniformtext_minsize=8,
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.info("都道府県と年と得たい情報を選択してください")          
          

# 複数年のタブ
with tab3:
    st.header("複数年")
    selected_columns_line = ["都道府県"]
    with st.expander("年"):
          year_line = st.multiselect("折れ線グラフで表示する年を指定してください",
                          list(range(2016, 2025)))
          
    # st.write(year_line)
    # st.write(want)


    if len(prefectures)>0 and len(year_df) > 0 and (len(want) > 0 or per == True):
        for i in year_line:
            for j in want:
                selected_columns_line.append(f"{i}/{j}")
            if per == True:
                selected_columns_line.append(f"{i}/舗装率")
        display = filtered[selected_columns_line]

       

        fig_line = go.Figure() # 土台
        # 各都道府県ごとにループを回す
        for idx, pre in enumerate(prefectures):
            # 都道府県ごとに色を固定（リストの数を超えたらループするように%を使ってcolorsのリスト番号を指定）
            color = colors[idx % len(colors)]

            # 現在のループの行だけを取得
            pre_data = display[display["都道府県"] == pre]
            
            # 実延長の描画
            if "実延長" in want:
                y_val = [pre_data[f"{y}/実延長"].values[0] for y in year_line]      #現在の行の選ばれた年の実延長の「数値」のみを入手
                fig_line.add_trace(go.Scatter(
                    x=year_line,
                    y=y_val,
                    name=f"{pre}/実延長",
                    mode="lines+markers",
                    line=dict(dash='solid', color=color),
                    yaxis="y1"
                ))
            
            # 舗装済延長の描画
            if "舗装済延長" in want:
                y_val = [pre_data[f"{y}/舗装済延長"].values[0] for y in year_line]      #現在の行の選ばれた年の舗装済延長の「数値」のみを入手
                fig_line.add_trace(go.Scatter(
                    x=year_line,
                    y=y_val,
                    name=f"{pre}/舗装済延長",
                    mode="lines+markers",
                    line=dict(dash='dash', color=color),
                    yaxis="y1"
                ))
            # 舗装率の描画（右軸）
            if per:
                y_val = [pre_data[f"{y}/舗装率"].values[0] for y in year_line]      #現在の行の選ばれた年の舗装率の「数値」のみを入手
                fig_line.add_trace(go.Scatter(
                    x=year_line,
                    y=y_val,
                    name=f"{pre}/舗装率",
                    mode="lines+markers",
                    line=dict(dash='dot', color=color),
                    yaxis="y2"
                ))                

        # レイアウト設定
        if per==True and len(want)==0:      # 舗装率のみの時
            fig_line.update_layout(
                yaxis=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 75] # 率は0-75に固定
                        ))
        else:                               # それ以外の時
            fig_line.update_layout(
            yaxis=dict(
                title="延長(km)",
                side="left"
                ),
            yaxis2=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 75] # 率は0-75に固定
                        ),
            )            
        fig_line.update_layout(
            title="複数年 道路状況比較",
            xaxis_title="年",
            legend=dict(
                title_text="凡例",  
                orientation="h",    # 凡例を横並びにする
                yanchor="top",      # 凡例の上を起点にする
                y=-0.3,              # グラフの下側
                xanchor="center",   # 凡例の中央を起点にする
                x=0.5,              # グラフの真ん中
            ),
            uniformtext_mode='hide',       # 小さすぎる数値テキストを隠す
            uniformtext_minsize=8,
        )

        st.plotly_chart(fig_line, use_container_width=True)

    else:
        st.info("都道府県と年と得たい情報を選択してください")          
