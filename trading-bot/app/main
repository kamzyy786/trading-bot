from fastapi import FastAPI
from pydantic import BaseModel
from app.signals import generate_signal
from app.ml_model import ml_filter_signal
from app.trade_executor import place_trade
from app.lot_sizing import calculate_lot_size

app = FastAPI()

class TradeRequest(BaseModel):
    symbol: str
    timeframe: str
    account_balance: float

@app.post("/trade")
def trade(req: TradeRequest):
    signal = generate_signal(req.symbol, req.timeframe)
    filtered = ml_filter_signal(signal, req.symbol)
    if filtered['action'] != 'WAIT':
        lot = calculate_lot_size(req.account_balance, 1.5, filtered['sl'], filtered['pip_value'])
        result = place_trade(req.symbol, filtered['action'], lot, filtered['sl'], filtered['tp'])
        return {"status": "executed", "details": result}
    return {"status": "no_trade"}
