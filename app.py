
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Risk Analyzer",
                   page_icon="📈",
                   layout="wide")

st.title("📈 Stock Return & Risk Analyzer")
st.write("Analyze stock performance using historical prices.")

stock = st.text_input("Stock name", "Sample Stock")

prices_input = st.text_input(
    "Enter closing prices separated by commas",
    "100, 102, 101, 105, 108, 106, 112"
)

if st.button("Analyze Stock"):
    try:
        prices = np.array(
            [float(x.strip()) for x in prices_input.split(",")]
        )

        if len(prices) < 2 or not np.all(np.isfinite(prices)):
            st.error("Enter at least two valid prices.")
        elif np.any(prices <= 0):
            st.error("Prices must be positive.")
        else:
            returns = pd.Series(prices).pct_change().dropna()

            total_return = (prices[-1] / prices[0] - 1) * 100
            avg_return = returns.mean() * 100
            volatility = returns.std(ddof=1) * np.sqrt(252) * 100

            st.subheader(f"Results for {stock}")

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Return", f"{total_return:.2f}%")
            c2.metric("Average Daily Return", f"{avg_return:.2f}%")
            c3.metric("Annualized Volatility", f"{volatility:.2f}%")

            chart_data = pd.DataFrame({
                "Observation": range(1, len(prices) + 1),
                "Closing Price": prices
            }).set_index("Observation")

            st.subheader("Stock Price Chart")
            st.line_chart(chart_data)

            st.subheader("Price Data")
            st.dataframe(
                pd.DataFrame({
                    "Observation": range(1, len(prices) + 1),
                    "Closing Price": prices
                }),
                use_container_width=True
            )

    except ValueError:
        st.error("Please enter numbers separated by commas.")
