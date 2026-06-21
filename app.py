import streamlit as st
from utils.stock_data import get_stock_info, get_stock_data
from utils.charts import create_candlestick_chart
from utils.indicators import add_indicators
from utils.predictions import predict_next_day
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Stock Market Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #050816,
        #0f172a,
        #111827
    );
}

/* Hide Streamlit default elements */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Title */
.main-title{
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:white;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:#94A3B8;
    font-size:18px;
    margin-bottom:40px;
}

/* Glass Card */
.glass-card{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);

    border: 1px solid rgba(255,255,255,0.1);

    border-radius:20px;

    padding:25px;

    box-shadow:
    0 8px 32px rgba(0,0,0,0.35);

    transition:0.3s;
}

.metric-title{
    color:#94A3B8;
    font-size:16px;
}

.metric-value{
    color:#00FF88;
    font-size:34px;
    font-weight:bold;
}

.company-card{
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:20px;
    color:white;
    border:1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class='main-title'>
📈 Stock Market Intelligence Platform
</div>

<div class='subtitle'>
AI Powered Market Analytics Dashboard
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# STOCK SEARCH
# --------------------------------------------------
st.subheader("🔍 Stock Search")

stock_options = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Tesla (TSLA)": "TSLA",
    "NVIDIA (NVDA)": "NVDA",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META"
}

selected_stock = st.selectbox(
    "Select Popular Stock",
    list(stock_options.keys())
)

symbol = stock_options[selected_stock]

st.write("Selected Stock:", symbol)
# --------------------------------------------------
# FETCH DATA
# -------------------------------------------------

try:

    info = get_stock_info(symbol)

    df = get_stock_data(symbol)

    df = add_indicators(df)
    predicted_price = predict_next_day(df)
    st.write(df.tail())
    st.write(df.columns)

    latest_rsi = round(df["RSI"].iloc[-1], 2)

    if latest_rsi < 30:
        trading_signal = "🟢 BUY"

    elif latest_rsi > 70:
        trading_signal = "🔴 SELL"

    else:
        trading_signal = "🟡 HOLD"
    latest_macd = round(df["MACD"].iloc[-1], 2)
    latest_macd_signal = round(
    df["MACD_SIGNAL"].iloc[-1], 2)

    company_name = info.get("longName", symbol)

    current_price = info.get("currentPrice", "N/A")
    market_cap = info.get("marketCap", 0)
    volume = info.get("volume", 0)
    pe_ratio = info.get("trailingPE", "N/A")

    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    ceo = info.get("companyOfficers", [{}])[0].get("name", "N/A")
    employees = info.get("fullTimeEmployees", "N/A")

except Exception as e:

    st.error(f"Error fetching stock data: {e}")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-title'>Current Price</div>
        <div class='metric-value'>${current_price}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-title'>Market Cap</div>
        <div class='metric-value'>{market_cap:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-title'>Volume</div>
        <div class='metric-value'>{volume:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class='glass-card'>
        <div class='metric-title'>P/E Ratio</div>
        <div class='metric-value'>{pe_ratio}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("---")

col_rsi1, col_rsi2 = st.columns(2)

with col_rsi1:
    st.metric(
        "RSI (14)",
        latest_rsi
    )

if latest_rsi > 70:
    rsi_signal = "🔴 OVERBOUGHT"
elif latest_rsi < 30:
    rsi_signal = "🟢 OVERSOLD"
else:
    rsi_signal = "🟡 NEUTRAL"

with col_rsi2:
    st.metric(
        "RSI Signal",
        rsi_signal
    )
if latest_rsi > 70:
    st.error("Stock may be overbought")

elif latest_rsi < 30:
    st.success("Stock may be oversold")

else:
    st.info("Stock is in a normal trading range")
st.subheader("📈 Trading Signal")

st.success(trading_signal)
st.markdown("---")

st.subheader("📊 MACD Analysis")

col_macd1, col_macd2 = st.columns(2)

with col_macd1:
    st.metric(
        "MACD",
        latest_macd
    )

with col_macd2:
    st.metric(
        "Signal Line",
        latest_macd_signal
    )
if latest_macd > latest_macd_signal:
    macd_signal = "🟢 BUY SIGNAL"
    st.success("MACD indicates bullish momentum")

elif latest_macd < latest_macd_signal:
    macd_signal = "🔴 SELL SIGNAL"
    st.error("MACD indicates bearish momentum")

else:
    macd_signal = "🟡 NEUTRAL"
    st.info("MACD is neutral")

st.metric(
    "MACD Signal",
    macd_signal
)
score = 0

if latest_rsi < 30:
    score += 1

if latest_macd > latest_macd_signal:
    score += 1

if score == 2:
    recommendation = "🟢 STRONG BUY"

elif score == 1:
    recommendation = "🟡 HOLD"

else:
    recommendation = "🔴 SELL"
st.subheader("🤖 AI Recommendation")

st.success(recommendation)
st.markdown("---")

st.subheader("🔮 AI Price Prediction")

st.metric(
    "Predicted Next Day Price",
    f"${predicted_price}"
)
# --------------------------------------------------
# COMPANY INFO
# --------------------------------------------------

st.markdown(f"""
<div class='company-card'>
    <h2>{company_name}</h2>
    <p><b>Sector:</b> {sector}</p>
    <p><b>Industry:</b> {industry}</p>
    <p><b>CEO:</b> {ceo}</p>
    <p><b>Employees:</b> {employees}</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

st.subheader("📊 Price Analysis")

chart = create_candlestick_chart(df, symbol)

st.plotly_chart(
    chart,
    width="stretch"
)
st.markdown("---")
st.subheader("💰 Investment Simulator")
investment_amount = st.number_input(
    "Enter Investment Amount ($)",
    min_value=100,
    value=1000
)
investment_date = st.date_input(
    "Investment Date"
)
try:

    start_price = df["Close"].iloc[0]

    current_price_sim = df["Close"].iloc[-1]

    shares = investment_amount / start_price

    current_value = shares * current_price_sim

    profit = current_value - investment_amount

    roi = (profit / investment_amount) * 100

    st.metric(
        "Current Value",
        f"${current_value:.2f}"
    )

    st.metric(
        "Profit/Loss",
        f"${profit:.2f}"
    )

    st.metric(
        "ROI %",
        f"{roi:.2f}%"
    )

except:
    st.warning("Unable to calculate investment performance")
st.markdown("---")
st.subheader("📊 Stock Comparison Tool")
compare_stock = st.selectbox(
    "Compare With",
    [
        "MSFT",
        "TSLA",
        "NVDA",
        "GOOGL",
        "AMZN",
        "META"
    ]
)
compare_info = get_stock_info(compare_stock)
col_a, col_b = st.columns(2)

with col_a:
    st.metric(
        symbol,
        info.get("currentPrice", "N/A")
    )

with col_b:
    st.metric(
        compare_stock,
        compare_info.get("currentPrice", "N/A")
    )