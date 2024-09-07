
import numpy as np
import pandas as pd


def periodReturn(series: pd.Series, period: str = None) -> pd.DataFrame:
    """
    Calculates periodic returns for the specified inputs

    Parameters
    ----------
    series : pd.Series
        price series
    period : str, optional
        None, defaults to daily frequency
        Sepcifiy W, M, Q and A for weekly, monthly, quarterly and annual frequency
    
    Returns
    -------
    pd.DataFrame
        resampled dataframe series of log returns
    """
    
    if period is None:
        temp = np.log(df).diff()
    
    if period == 'week':
        df = df.resample('W').last()
        temp = np.log(df).diff()
    
    if period == 'month':
        df = df.resample('M').last()
        temp = np.log(df).diff()
    
    if period == 'quarter':
        df = df.resample('Q').last()
        temp = np.log(df).diff()
    
    if period == 'annual':
        df = df.resample('A').last()
        temp = np.log(df).diff()

    if period == 'all':
        temp = pd.DataFrame({
            'daily': dailyReturn(df).iloc[-1],
            'week': weeklyReturn(df).iloc[-1],
            'month': monthlyReturn(df).iloc[-1],
            'quarter': quarterlyReturn(df).iloc[-1],
            'annual': annualReturn(df).iloc[-1]
            }, index=[df.index[-1]])

    return temp.dropna()


def dailyReturn(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates daily returns for the specified inputs."""
    return periodReturn(df)


def weeklyReturn(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates weekly returns for the specified inputs."""
    return periodReturn(df, period='week')


def monthlyReturn(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates monthly returns for the specified inputs."""
    return periodReturn(df, period='month')


def quarterlyReturn(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates quarterly returns for the specified inputs."""
    return periodReturn(df, period='quarter')


def annualReturn(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates annual returns for the specified inputs."""
    return periodReturn(df, period='annual')   


def allReturn(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates annual returns for the specified inputs."""
    return periodReturn(df, period='all')


def cagr(returns: pd.Series, intra_period: int = 1, is_log: bool = False) -> float:
    """
    Compounded Annual Growth Rate (CAGR) is the annual rate of return

    Parameters
    ----------
    returns : pd.Series
        price series
    intra_period : int, optional
        period of intra-period returns, defaults to 1 for annual timeframe
    is_log : bool, optional
        defaults to False if its simple return
    
    Returns
    -------
    float
        returns CAGR for the specified period

    Notes
    -----
        CAGR = (Ending Value / Starting Value)^(1/n) - 1

            Ending Value = Begging Value 
            Starting Value = Ending Value 
            n = period of intra-period returns
    """
    
    if is_log:
        cumulative_returns = np.exp(returns.sum())      # for log returns        
        years = len(returns)/(252*intra_period) 
        return (cumulative_returns[-1])**(1/years) - 1
    else:
        cumulative_returns = (1 + returns).cumprod()    # for simple returns
        
    years = len(returns)/(252*intra_period) 
    return (cumulative_returns[-1])**(1/years) - 1  


def volatility(returns: pd.Series, intra_period: int = 1) -> float:
    """
    Annualized volatility is key risk metrics

    Parameters
    ----------
    returns : pd.Series
        price series
    intra_period : int, optional
        period of intra-period returns, defaults to 1 for annual timeframe

    Returns
    -------
    float
        returns annualized volatility

    Notes
    -----
        Annualization is achieved by multiplying volatility with square root of
        a) 252 to annualize daily volatility
        b) 52 to annualize weekly volatility
        c) 12 to annualize monthly volatility
    """
    return returns.std()*np.sqrt(252*intra_period)


def sharpe(returns:pd.Series, is_log: bool = False, rf: float = 0.0) -> float:
    """
    Sharpe ratio is the average return earned in excess of the risk free return
    for every unit of volatility. This is one of the most widely used meausre of
    risk adjusted return. Sharpe ration greater than 1 is considered to be good.

    Parameters
    ----------
    returns : pd.Series
        price series
    is_log : bool, optional
        defaults to False if its simple return
    rf : float, optional
        RiskFree rate of return, defaults to 0.

    Returns
    -------
    float
        returns sharpe ratio

    Notes
    -----
        Sharpe Ratio = (Expected Return - RiskFree Return) / Volatility of Returns
    """
    return (cagr(returns, is_log = False) - rf) / volatility(returns)


def maxdd(returns: pd.Series, is_log: bool = False) -> float:
    """
    A maximum drawdown (MDD) is an indicator of downside risk and measures the
    largest percentage drop of the cumulative return over a specified time period.

    Parameters
    ----------
    returns : pd.Series
        price series
    is_log : bool, optional
        defaults to False if its simple return

    Returns
    -------
    float
        returns MDD for the specified period in percentage

    Notes
    -----
        It observes the maximum loss from a peak to a trough of a portfolio before
        a new peak is attained.

        MDD = (Peak Value - Lowest Value) / Peak Value

            Peak Value = Highest Value of the cumulative return
            Lowest Value = Lowest Value of the cumulative return    
    """    
    if is_log:
        cumulative_returns = np.exp(returns.sum())      # for log returns        
    else:
        cumulative_returns = (1 + returns).cumprod()    # for simple returns
    
    drawdown_percentage = (cumulative_returns.cummax() - cumulative_returns) / cumulative_returns.cummax()
    return drawdown_percentage.max() 


def calmar(returns: pd.Series, is_log: bool = False) -> float:
    """
    Ratio of compounded annual growth rate and maximum drawdown. It is a measure
    of risk adjusted return. Lower the ratio, the worse the performance on a
    risk-adjusted basis.

    Parameters
    ----------
    returns : pd.Series
        price series
    is_log : bool, optional
        defaults to False if its simple return

    Returns
    -------
    float
        returns calmar ratio

    Notes
    -----
        Calmar Ratio = CAGR / MDD

        CAGR = (Ending Value / Starting Value)^(1/n) - 1
        MDD = (Peak Value - Lowest Value) - Peak Value
    """
    return cagr(returns, is_log = False)/maxdd(returns, is_log = False)