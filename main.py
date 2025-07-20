# WebApp Algorithmic Trading Bot for Gold and Bitcoin using Price Action & Smart Money Concepts

# === OVERVIEW ===
# Tech Stack: Python (FastAPI) + React (Frontend) + PostgreSQL (Logs) + ML (PyTorch/TensorFlow)
# Features:
# 1. SMC + Price Action based signal engine
# 2. Trade automation with dynamic lot sizing
# 3. ML modules for signal filtering and risk optimization
# 4. Real-time broker API integration (Exness/Binance)

# === BACKEND STRUCTURE ===
# Project folders:
# ├── app/
# │   ├── main.py              # FastAPI main app
# │   ├── signals.py           # Signal generation logic
# │   ├── ml_model.py          # ML model loader/predictor
# │   ├── trade_executor.py    # Broker API integration
# │   ├── lot_sizing.py        # Lot sizing logic
# │   └── utils.py             # Helper functions
# └── data/
#     └── historical/          # 1Y OHLCV data for BTC/XAU

# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.signals import generate_signal
from app.trade_executor import place_trade
from app.lot_sizing import calculate_lot_size
from app.ml_model import ml_filter_signal

app = FastAPI()

class TradeRequest(BaseModel):
    symbol: str  # 'XAUUSD' or 'BTCUSDT'
    timeframe: str  # e.g. '15m'
    account_balance: float

@app.post("/trade")
def trade_logic(req: TradeRequest):
    try:
        signal = generate_signal(req.symbol, req.timeframe)
        filtered = ml_filter_signal(signal, req.symbol)

        if filtered['action'] != 'WAIT':
            lot = calculate_lot_size(
                req.account_balance,
                risk_pct=1.5,
                stop_loss_pips=filtered['sl'],
                pip_value=filtered['pip_value']
            )
            result = place_trade(
                symbol=req.symbol,
                action=filtered['action'],
                lot=lot,
                stop_loss=filtered['sl'],
                take_profit=filtered['tp']
            )
            return {"status": "executed", "details": result}
        return {"status": "no_trade"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === SIGNAL GENERATION ===
# signals.py (simplified)
import pandas as pd

def generate_signal(symbol, timeframe):
    df = load_ohlcv(symbol, timeframe)
    # Logic for SMC: Order Block, BOS, FVG, Liquidity grab
    ob_zone = detect_order_block(df)
    bos = detect_bos(df)
    fvg = detect_fvg(df)

    if bos and fvg and ob_zone:
        return {"action": "BUY", "sl": 50, "tp": 100, "pip_value": 1}
    return {"action": "WAIT"}

# === ML FILTERING ===
# ml_model.py (simplified)
import joblib

model = joblib.load("data/models/signal_filter_model.pkl")

def ml_filter_signal(signal, symbol):
    if signal['action'] == 'WAIT':
        return signal
    # Example input vector: [price diff, OB dist, FVG size, vol, RSI]
    features = extract_features(symbol)
    prediction = model.predict([features])[0]
    if prediction == 1:
        return signal
    return {"action": "WAIT"}

# === LOT SIZING ===
# lot_sizing.py

def calculate_lot_size(balance, risk_pct, stop_loss_pips, pip_value):
    risk = balance * (risk_pct / 100)
    lot = risk / (stop_loss_pips * pip_value)
    return round(lot, 2)

# === TRADE EXECUTOR ===
# trade_executor.py
import requests

EXNESS_API = "https://api.exness.com/trade"

def place_trade(symbol, action, lot, stop_loss, take_profit):
    # Example payload structure for broker
    payload = {
        "symbol": symbol,
        "type": "buy" if action == 'BUY' else 'sell',
        "volume": lot,
        "sl": stop_loss,
        "tp": take_profit
    }
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    r = requests.post(EXNESS_API, json=payload, headers=headers)
    return r.json()

# === FRONTEND REACT (Brief Description) ===
# Pages:
# - Dashboard: Shows signals, live trades, equity
# - Settings: Broker keys, risk %, asset selection
# - Trade Logs: View past executed trades

# React fetch example:
# fetch('/trade', {
#   method: 'POST',
#   body: JSON.stringify({ symbol: 'XAUUSD', timeframe: '15m', account_balance: 5000 }),
#   headers: { 'Content-Type': 'application/json' }
# })

# === DEPLOYMENT ===
# Use Docker for backend containerization
# Host backend on Render/AWS Lambda
# Frontend on Vercel/Netlify

# This system provides an end-to-end trading bot framework focused on SMC + price action + ML filtering.
