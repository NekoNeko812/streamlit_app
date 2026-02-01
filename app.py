import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")       # 横幅をブラウザに合わせる


st.title("都道府県別道路の実延長と舗装済延長の推移")
st.write("test")

df = pd.read_csv("都道府県別道路の実延長と舗装済延長.csv", encoding="shift_jis")

with st.sidebar:
  st.subheader("表示する情報")
  prefectures = st.multiselect("検索したい都道府県を選択してください（複数選択可）",
                          df["都道府県"].unique())
  want = st.multiselect("得たい情報を選択してください",
                            ["実延長", "舗装済延長"])
  per = st.checkbox("舗装率は表示しますか？", value=False)

filtered = df[df["都道府県"].isin(prefectures)]

tab1, tab2, tab3 = st.tabs(["表", "指定年", "複数年"])

# 表のタブ
with tab1:
    st.header("表")
    selected_columns_df = ["都道府県"]

    with st.expander("年"):
          year_df = st.multiselect("表で表示する年を指定してください",
                          list(range(2016, 2025)))


    st.write(year_df)
    st.write(want)

    for i in year_df:
        for j in want:
            selected_columns_df.append(f"{i}/{j}")
        if per == True:
            selected_columns_df.append(f"{i}/舗装率")



    if len(year_df) > 0 and (len(want) > 0 or per == True):
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
    
    st.write(year_bar)
    st.write(want)


    if len(want) > 0 or per == True:
        for j in want:
            selected_columns_bar.append(f"{year_bar}/{j}")
            
        if per == True:
            selected_columns_bar.append(f"{year_bar}/舗装率")
        display = filtered[selected_columns_bar]
        st.write("単位：km")
        
       

        fig_bar = go.Figure() # 土台
        if per != True or (len(want) == 0 and per == True):
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
        else:
            colmuns_perin=[]
            for i in want:
                colmuns_perin.append(f"{year_bar}/{i}")
            for col in colmuns_perin:                
                fig_bar.add_trace(go.Bar(
                x=display["都道府県"],
                y=display[col],
                name=col.split("/")[-1],
                text=display[col],
                textposition="auto",
                yaxis="y1",
                ))

            fig_bar.add_trace(go.Scatter(
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
        if per==True and len(want)==0:
            fig_bar.update_layout(
                yaxis=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 100] # 率は0-100に固定
                        ))
        else:
            fig_bar.update_layout(
            yaxis=dict(
                title="延長",
                side="left"
                ),
            yaxis2=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 100] # 率は0-100に固定
                        ),
            )            
        fig_bar.update_layout(
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
        st.info("年と得たい情報を選択してください")          
          

# 複数年のタブ
with tab3:
    st.header("複数年")
    selected_columns_line = ["都道府県"]
    with st.expander("年"):
          year_line = st.multiselect("折れ線グラフで表示する年を指定してください",
                          list(range(2016, 2025)))
          
    st.write(year_line)
    st.write(want)


    if (len(want) > 0 or per == True) and len(year_line) != 0 :
        for i in year_line:
            for j in want:
                selected_columns_line.append(f"{i}/{j}")
            if per == True:
                selected_columns_line.append(f"{i}/舗装率")
        display = filtered[selected_columns_line]
        st.write("単位：km")
        
       

        fig_line = go.Figure() # 土台
        # 延長
        if "実延長" in want:
        #選択された項目ごとに「棒の情報」を一つずつ足していくコード
            for pre in prefectures:
                for i in year_line:
                    fig_line.add_trace(go.Scatter(
                        x=year_line,
                        y=display[f"{i}/実延長"],
                        name=f"{pre}の実延長",
                        text=display[f"{i}/実延長"],
                        yaxis="y1",
                        mode="markers+lines",                  
                    ))
                # 延長
        if "舗装済延長" in want:
        #選択された項目ごとに「棒の情報」を一つずつ足していくコード
            for pre in prefectures:
                for i in year_line:
                    fig_line.add_trace(go.Scatter(
                        x=year_line,
                        y=display[f"{i}/舗装済延長"],
                        name=f"{pre}の舗装済延長",
                        text=display[f"{i}/舗装済延長"],
                        yaxis="y1",
                        mode="markers+lines",
                    )
                    )
        if per == True:
        #選択された項目ごとに「棒の情報」を一つずつ足していくコード
            for pre in prefectures:
                for i in year_line:
                    fig_line.add_trace(go.Scatter(
                        x=year_line,
                        y=display[f"{i}/舗装率"],
                        name=f"{pre}の舗装率",
                        text=display[f"{i}/舗装率"],
                        yaxis="y2",
                        mode="markers+lines"
                    ))

        # レイアウト設定
        if per==True and len(want)==0:
            fig_line.update_layout(
                yaxis=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 100] # 率は0-100に固定
                        ))
        else:
            fig_line.update_layout(
            yaxis=dict(
                title="延長",
                side="left"
                ),
            yaxis2=dict(title="舗装率(%)",
                        overlaying="y",
                        side="right",
                        range=[0, 100] # 率は0-100に固定
                        ),
            )            
        fig_line.update_layout(
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
        st.info("年と得たい情報を選択してください")          
    # if len(want) > 0 or per != True and len(year_line) > 0:
    #     display = filtered[selected_columns_line]
    #     st.write("単位：km")
        
    #     value_cols_line = [c for c in selected_columns_line if c != "都道府県"]

    #     fig_line = go.Figure() # 土台

    #     #選択された項目ごとに「棒の情報」を一つずつ足していくコード
    #     fig_line.add_trace(go.Scatter(
    #             x=year_line,
    #             y=display[value_cols_line],
    #             mode="lines+markers",
    #             name=value_cols_line,
    #             text=display[value_cols_line],
    #             textposition="auto"
    #         ))

    #     # レイアウト設定
    #     fig_line.update_layout(
    #         title=f"{year_line[1]}年~{year_line[-1]}年 道路状況比較",
    #         xaxis_title="年",
    #         yaxis_title="延長",
    #         legend_title="項目",
    #         uniformtext_mode='hide',       # 小さすぎる数値テキストを隠す
    #         uniformtext_minsize=8,
    #     )

    #     st.plotly_chart(fig_line, use_container_width=True)

    # else:
    #     st.info("年と得たい情報を選択してください") 