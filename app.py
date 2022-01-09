import yfinance as yf
import altair as alt
import streamlit as st


@st.cache
def get_data(ticker):
    tk = yf.Ticker(ticker)
    df = tk.history(period='3y')
    df = df[['Close']]
    df = df.reset_index()
    return df


def get_chart(df):
    chart = (alt.Chart(df).mark_line(opacity=0.8, clip=True).encode(
        x="Date:T",
        y=alt.Y(
            "Close:Q",
            stack=None,
            scale=alt.Scale(
                domain=[df.min()['Close'] * 0.99,
                        df.max()['Close'] * 1.01])),
    ))
    return chart


st.title('株価可視化アプリ')

st.sidebar.write("""
# 直近３年間の株価遷移
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## ティッカーシンボル選択
""")

tickers = [
    'GOOGL',
    'AAPL',
    'FB',
    'AMZN',
    'MSFT',
]

ticker = st.sidebar.selectbox('ティッカー', tickers)

st.write(f"""
### **{ticker}** 直近３年間の株価遷移
""")

df = get_data(ticker)
st.write("### 株価 (USD)", df)

st.altair_chart(get_chart(df), use_container_width=True)
