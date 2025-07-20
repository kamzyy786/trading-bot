def place_trade(symbol, action, lot, stop_loss, take_profit):
    return {
        "symbol": symbol,
        "action": action,
        "lot": lot,
        "sl": stop_loss,
        "tp": take_profit
    }