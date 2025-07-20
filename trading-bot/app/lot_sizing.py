def calculate_lot_size(balance, risk_pct, stop_loss_pips, pip_value):
    risk = balance * (risk_pct / 100)
    return round(risk / (stop_loss_pips * pip_value), 2)