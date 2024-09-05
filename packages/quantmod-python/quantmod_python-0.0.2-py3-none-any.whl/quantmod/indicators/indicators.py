import pandas as pd

def ATR(df: pd.DataFrame, lookback: int = 14) -> pd.Series:
    """
    Calculate the Average True Range (ATR).

    ATR is a volatility indicator that measures the average of the true range values
    over a specified period. An expanding ATR indicates increased volatility, while
    a low ATR value indicates a series of periods with small price ranges.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with OHLC (Open, High, Low, Close) price data.
    lookback : int, optional
        Number of periods to use for ATR calculation, by default 14.

    Returns
    -------
    pd.Series
        A pandas Series containing the ATR values for each period.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'Open': [10, 11, 12],
    ...     'High': [12, 13, 14],
    ...     'Low': [9, 10, 11],
    ...     'Close': [11, 12, 13]
    ... })
    >>> atr = ATR(df, lookback=2)
    >>> print(atr)
    0         NaN
    1    3.000000
    2    2.750000
    dtype: float64
    """
    
    df = df.copy()
    
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Close'].shift(1))
   
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR']=df['TR'].rolling(lookback).mean()
    
    data = df.drop(['H-L','H-PC','L-PC'],axis=1) # drop columns
    
    return data['ATR']
