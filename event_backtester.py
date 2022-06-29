"""
macro/scenario/event backtester
"""

import pandas as pd
from typing import List
import numpy as np
import datetime as dt


def derive_backtest_results(data: pd.DataFrame, days: List[int]) -> pd.DataFrame:
    """
    creates the weighted return (if weight col provided) for x # of days in the future by column for days in day list
    """
    if "weights" not in data.columns:
        data["weights"] = 1

    for day in days:
        data[f"close_{day}"] = (data["close"].shift(-day) - data["close"]) / (data["close"]) * data["weights"]  # % returns over n days

    return data


def return_signal_days(data: pd.DataFrame, days=None) -> pd.DataFrame:
    """
    returns the returns for x # of days in the future columns when the signal is equal to 1
    """
    return_columns = ["date"] + [f"close_{day}" for day in days] if days is not None else data.columns
    return data[data["signal"] != 0].reindex(columns=return_columns)


def calculate_average_for_time(data: pd.DataFrame, days: List[int]) -> List[object]:
    """
    calculates the mean % return for x days in the future for the dataset provided (sliced in derive average data function)
    """
    data = return_signal_days(data, days)
    return [np.nanmean(data[x]) for x in data.columns if "close_" in x]


def derive_average_data(data: pd.DataFrame, days: List[int], averages: List[int]) -> List[float]:
    """
    breaks the data down by averages list, i.e. x # of years in the past, runs the mean function for all x % return for
    n days in the futre and appends results to dataframe
    """
    NUMERICAL_AVERAGE_YEARS = [1, 5, 10, 20]
    DAYS_IN_YEAR = 365
    output_data = pd.DataFrame()
    append_columns = ["type"] + [x for x in data.columns if "close_" in x]

    if "ALL" in averages:  # have to break this out into a special case because it is a non number
        appending_row = ["ALL"] + calculate_average_for_time(data, days)
        appending_data = pd.DataFrame([appending_row], columns=append_columns)
        output_data = output_data.append([appending_row], ignore_index=True) if not output_data.empty else appending_data

    for year_num in NUMERICAL_AVERAGE_YEARS:  # appending the averages for numerical years
        date_parse_condition = data[data["date"] > data.loc[data.index[-1], "date"]-dt.timedelta(DAYS_IN_YEAR*year_num)]
        appending_row = [f"{year_num} Year Average"] + calculate_average_for_time(date_parse_condition, days)
        appending_data = pd.DataFrame([appending_row], columns=append_columns)
        output_data = output_data.append(appending_data, ignore_index=True) if not output_data.empty else appending_data

    return output_data


if __name__ == "__main__":
    test_data = pd.read_csv(r"C:\Users\bnewe\OneDrive\Desktop\ES.csv")
    test_days = [1, 2, 5, 20, 40, 60, 100, 120, 240]
    average_list = ["ALL"] + [1, 5, 10, 20]
    test_data = derive_backtest_results(test_data, test_days)
    x_data = derive_average_data(test_data, average_list)


