import pandas as pd
from ssafc_strategy import is_green_ssafc_candle, is_red_ssafc_candle, ssafc_strategy

def test_is_green_ssafc_candle():
    green_candle = pd.Series({'Open': 100, 'High': 110, 'Low': 100, 'Close': 108})
    assert is_green_ssafc_candle(green_candle)

def test_is_red_ssafc_candle():
    red_candle = pd.Series({'Open': 115, 'High': 115, 'Low': 105, 'Close': 106})
    assert is_red_ssafc_candle(red_candle)

def test_ssafc_strategy():
    data = pd.read_csv('data.csv')
    signals = ssafc_strategy(data)
    assert len(signals) == 2

    # Check the first signal (Buy)
    assert signals.iloc[0]['Type'] == 'Buy'
    assert round(signals.iloc[0]['Entry'], 2) == 120.91

    # Check the second signal (Sell)
    assert signals.iloc[1]['Type'] == 'Sell'
    assert round(signals.iloc[1]['Entry'], 2) == 108.78
