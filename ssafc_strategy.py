import pandas as pd

def is_green_ssafc_candle(candle):
    """
    Checks if a candle is a Green SSAFC candle.
    """
    return (
        candle['Close'] > candle['Open'] and
        candle['Open'] == candle['Low'] and
        (candle['Close'] - candle['Open']) >= 0.8 * (candle['High'] - candle['Low']) and
        (candle['High'] - candle['Close']) <= 0.2 * (candle['High'] - candle['Low'])
    )

def is_red_ssafc_candle(candle):
    """
    Checks if a candle is a Red SSAFC candle.
    """
    return (
        candle['Close'] < candle['Open'] and
        candle['Open'] == candle['High'] and
        (candle['Open'] - candle['Close']) >= 0.8 * (candle['High'] - candle['Low']) and
        (candle['Close'] - candle['Low']) <= 0.2 * (candle['High'] - candle['Low'])
    )

def is_white_area(data, entry, stoploss, current_index):
    """
    Checks if the Entry-Stoploss zone is a fresh/untouched (white) area.
    """
    for i in range(current_index):
        prev_candle = data.iloc[i]
        if not (prev_candle['High'] < min(entry, stoploss) or prev_candle['Low'] > max(entry, stoploss)):
            return False
    return True

def calculate_atr(data, period=14):
    """
    Calculates the Average True Range (ATR).
    """
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift())
    low_close = abs(data['Low'] - data['Close'].shift())

    tr = high_low.combine(high_close, max).combine(low_close, max)
    atr = tr.ewm(span=period, adjust=False).mean()
    return atr

def ssafc_strategy(data):
    """
    Implements the SSAFC trading strategy.
    """
    signals = []
    atr = calculate_atr(data)

    for i in range(1, len(data)):
        candle = data.iloc[i]

        if is_green_ssafc_candle(candle):
            entry = candle['Open'] + 0.1 * atr.iloc[i]
            stoploss = candle['Open'] - 0.1 * atr.iloc[i]
            if is_white_area(data, entry, stoploss, i):
                signals.append({'Type': 'Buy', 'Entry': entry, 'Stoploss': stoploss})

        elif is_red_ssafc_candle(candle):
            entry = candle['Open'] - 0.1 * atr.iloc[i]
            stoploss = candle['Open'] + 0.1 * atr.iloc[i]
            if is_white_area(data, entry, stoploss, i):
                signals.append({'Type': 'Sell', 'Entry': entry, 'Stoploss': stoploss})

    return pd.DataFrame(signals)

if __name__ == "__main__":
    # data = pd.read_csv('data.csv')  # Uncomment to use a CSV file
    # signals = ssafc_strategy(data)
    # print(signals)
    pass
