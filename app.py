5:13 PM
from flask import Flask, render_template, request
import yfinance as yf

app = Flask(_name_)

@app.route("/", methods=["GET", "POST"])
def home():
    symbol = request.form.get("symbol", "AAPL").upper()
    result = None

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1mo")

        if data.empty:
            result = {"error": "Hindi makita ang stock symbol."}
        else:
            price = float(data["Close"].iloc[-1])
            ma5 = float(data["Close"].tail(5).mean())
            ma20 = float(data["Close"].mean())

            if ma5 > ma20:
                signal = "📈 UP / BULLISH"
            elif ma5 < ma20:
                signal = "📉 DOWN / BEARISH"
            else:
                signal = "➡️ NEUTRAL"

            result = {
                "symbol": symbol,
                "price": round(price, 2),
                "ma5": round(ma5, 2),
                "ma20": round(ma20, 2),
                "signal": signal
            }

    except Exception as e:
        result = {"error": str(e)}

    return render_template("index.html", result=result)


if _name_ == "_main_":
    app.run(host="0.0.0.0", port=8080)
