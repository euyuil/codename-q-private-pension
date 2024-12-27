from dataclasses import dataclass
from datetime import date
from typing import List

import numpy as np
import pandas as pd
import xarray as xr

@dataclass
class EvaluationPeriod:
    label: str
    start_date: date
    end_date: date

@dataclass
class EvaluationResult:
    period: EvaluationPeriod
    observations: int
    open: float
    high: float
    low: float
    close: float
    annualized_return: float
    annualized_volatility: float
    sharpe_ratio: float
    max_drawdown: float

def move_month(date, months: int) -> pd.Timestamp:
    """
    Move the given date by a number of months.

    Args:
        date: The original date.
        months: The number of months to move.

    Returns:
        A new date moved by the specified number of months.
    """
    date = pd.Timestamp(date)
    new_total_months = date.year * 12 + date.month - 1 + months
    new_year = new_total_months // 12
    new_month = new_total_months % 12 + 1
    new_day = date.day
    return pd.Timestamp(year=new_year, month=new_month, day=new_day)

def get_evaluation_periods(start_date, end_date) -> List[EvaluationPeriod]:
    """
    Get a list of evaluation periods between the start and end dates.

    Args:
        start_date: The start date.
        end_date: The end date.

    Returns:
        A list of EvaluationPeriod objects.
    """
    periods: List[EvaluationPeriod] = []
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    periods.append(EvaluationPeriod("ITD", start_date, end_date))

    ytd_start_date = pd.Timestamp(f"{end_date.year}-01-01")
    if ytd_start_date >= start_date:
        periods.append(EvaluationPeriod("YTD", ytd_start_date, end_date))

    qtd_start_date = pd.Timestamp(f"{end_date.year}-{(end_date.month - 1) // 3 * 3 + 1}-01")
    if qtd_start_date >= start_date:
        periods.append(EvaluationPeriod("QTD", qtd_start_date, end_date))

    mtd_start_date = pd.Timestamp(f"{end_date.year}-{end_date.month}-01")
    if mtd_start_date >= start_date:
        periods.append(EvaluationPeriod("MTD", mtd_start_date, end_date))

    for label, months in [("1M", 1), ("3M", 3), ("6M", 6), ("1Y", 12), ("3Y", 36), ("5Y", 60), ("10Y", 120)]:
        period_start_date = move_month(end_date, -months)
        if period_start_date >= start_date:
            periods.append(EvaluationPeriod(label, period_start_date, end_date))

    return sorted(periods, key=lambda period: period.start_date)

def is_leap_year(year: int) -> bool:
    """
    Check if a year is a leap year.

    Args:
        year: The year to check.

    Returns:
        True if the year is a leap year, False otherwise.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_days_in_year(year: int) -> int:
    """
    Get the number of days in a year.

    Args:
        year: The year.

    Returns:
        The number of days in the year.
    """
    return 366 if is_leap_year(year) else 365

def get_years_between_dates(start_date, end_date) -> float:
    """
    Calculate the number of years between two dates.

    Args:
        start_date: The start date.
        end_date: The end date.

    Returns:
        The number of years between the start and end dates.
    """
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    if start_date > end_date:
        raise ValueError("start_date must be earlier than end_date")

    start_year = start_date.year
    start_yday = start_date.timetuple().tm_yday
    end_year = end_date.year
    end_yday = end_date.timetuple().tm_yday

    years = 1 - start_yday / get_days_in_year(start_year)
    years += end_yday / get_days_in_year(end_year)
    years += end_year - start_year - 1
    return years

def get_annualized_return(da: xr.DataArray) -> xr.DataArray:
    """
    Calculate the annualized return for each security.

    Args:
        da: DataArray with dimensions of (datetime, security).

    Returns:
        DataArray with dimensions of (security) containing annualized returns.
    """
    years = get_years_between_dates(da.datetime[0].item(), da.datetime[-1].item())
    return (da[-1] / da[0]) ** (1 / years) - 1

def get_annualized_volatility(da: xr.DataArray) -> xr.DataArray:
    """
    Calculate the annualized volatility for each security.

    Args:
        da: DataArray with dimensions of (datetime, security).

    Returns:
        DataArray with dimensions of (security) containing annualized volatilities.
    """
    n = da.count(dim="datetime")
    years = get_years_between_dates(da.datetime[0].item(), da.datetime[-1].item())
    n_per_year = n / years
    r = np.log(da / da.shift(datetime=1))
    r_bar = r.sum(dim="datetime") / (n - 1)
    sigma_daily = np.sqrt(((r - r_bar) ** 2).sum(dim="datetime") / (n - 2))
    sigma_annual = sigma_daily * (n_per_year ** 0.5)
    return sigma_annual

def get_sharpe_ratio(da: xr.DataArray, risk_free_rate: float) -> xr.DataArray:
    """
    Calculate the Sharpe ratio for each security.

    Args:
        da: DataArray with dimensions of (datetime, security).
        risk_free_rate: The risk-free rate.

    Returns:
        DataArray with dimensions of (security) containing Sharpe ratios.
    """
    annualized_return = get_annualized_return(da)
    annualized_volatility = get_annualized_volatility(da)
    return (annualized_return - risk_free_rate) / annualized_volatility

def get_max_drawdown(da: xr.DataArray) -> xr.DataArray:
    """
    Calculate the maximum drawdown for each security.

    Args:
        da: DataArray with dimensions of (datetime, security).

    Returns:
        DataArray with dimensions of (security) containing maximum drawdowns.
    """
    max_price = da.rolling(datetime=da.datetime.size, min_periods=1).max()
    drawdown = da / max_price - 1
    return -drawdown.min(dim="datetime")

def get_evaluation_result(da: xr.DataArray, period: EvaluationPeriod) -> EvaluationResult:
    """
    Calculate evaluation results for a given period.

    Args:
        da: DataArray with dimensions of (datetime, security).
        period: The evaluation period.

    Returns:
        An EvaluationResult object containing the results.
    """
    mask = (da.datetime >= period.start_date) & (da.datetime <= period.end_date)
    da = da.sel(datetime=mask)
    return EvaluationResult(
        period=period,
        observations=da.count().item(),
        open=da[0].item(),
        high=da.max(dim="datetime").item(),
        low=da.min(dim="datetime").item(),
        close=da[-1].item(),
        annualized_return=get_annualized_return(da).item(),
        annualized_volatility=get_annualized_volatility(da).item(),
        sharpe_ratio=get_sharpe_ratio(da, 0.025).item(),
        max_drawdown=get_max_drawdown(da).item()
    )

def get_evaluation_results(da: xr.DataArray) -> List[EvaluationResult]:
    """
    Calculate evaluation results for different periods.

    Args:
        da: DataArray with dimensions of (datetime, security).

    Returns:
        A list of EvaluationResult objects containing the results for different periods.
    """
    periods = get_evaluation_periods(da.datetime[0].item(), da.datetime[-1].item())
    results = []
    for period in periods:
        try:
            result = get_evaluation_result(da, period)
            results.append(result)
        except Exception as e:
            print(f"Error processing period {period.label}: {e}")
    return results
