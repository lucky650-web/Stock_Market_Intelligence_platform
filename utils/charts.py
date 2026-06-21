import plotly.graph_objects as go


def create_candlestick_chart(df, symbol):

    fig = go.Figure()

    # Candles
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        )
    )

    # SMA 20
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA20"],
            name="SMA 20",
            line=dict(width=2)
        )
    )

    # SMA 50
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA50"],
            name="SMA 50",
            line=dict(width=2)
        )
    )

    # SMA 200
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA200"],
            name="SMA 200",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        title=f"{symbol} Technical Analysis",
        template="plotly_dark",
        height=700,
        xaxis_rangeslider_visible=False
    )

    return fig