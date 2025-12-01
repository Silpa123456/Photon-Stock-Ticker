import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ---------- Page setup ----------
st.set_page_config(
    page_title="Photon - Real-time Stock Ticker",
    layout="centered"
)

st.title("📈 Photon - Real-time Stock Ticker")
st.write("Live stock price updates (using Streamlit)")

# Initial mock stock prices
tickers = {
    "AAPL": 150.0,
    "GOOGL": 2800.0,
    "TSLA": 700.0,
    "MSFT": 320.0,
}

last_prices = {}
placeholder = st.empty()

while True:
    # ---- update prices ----
    updated = {}
    for name, price in tickers.items():
        change = random.uniform(-2, 2)
        new_price = round(price + change, 2)
        updated[name] = new_price
        tickers[name] = new_price

    # ---- build rows HTML with colors ----
    rows_html = ""
    for ticker, new_price in updated.items():
        if ticker in last_prices:
            old = last_prices[ticker]
            if new_price > old:
                color = "limegreen"
            elif new_price < old:
                color = "red"
            else:
                color = "white"
        else:
            color = "white"

        rows_html += f"""
        <tr>
            <td>{ticker}</td>
            <td style="color:{color}; font-weight:bold;">{new_price}</td>
        </tr>
        """

    last_prices = updated

    # ---- complete HTML for the table ----
    full_html = f"""
    <style>
      body {{
        background-color: #0e1117;
        color: white;
        font-family: system-ui, sans-serif;
      }}
      table.stock-table {{
        border-collapse: collapse;
        margin: auto;
        min-width: 320px;
        background-color: #111;
      }}
      .stock-table th, .stock-table td {{
        border: 1px solid #555;
        padding: 8px 14px;
        text-align: center;
        color: white;
      }}
      .stock-table th {{
        background-color: #222;
      }}
    </style>

    <table class="stock-table">
      <tr>
        <th>Ticker</th>
        <th>Price (USD)</th>
      </tr>
      {rows_html}
    </table>
    """

    # ---- render HTML inside placeholder ----
    with placeholder.container():
        components.html(full_html, height=260)

    time.sleep(1)



