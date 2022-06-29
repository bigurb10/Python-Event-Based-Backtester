"""
contains the generic functions/globals for dash app buildouts.
"""

from typing import Tuple
import datetime as dt
from abc import ABC, abstractmethod
from dash import Dash
import dash_html_components as html
import pandas as pd
from typing import List, Dict
import holidays

EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

TAB_STYLE = {}


class DashboardTab(ABC):
    def __init__(self, display_name: str, internal_name: str):
        self.display_name = display_name
        self.internal_name = internal_name

    @abstractmethod
    def get_html(self):
        pass

    @abstractmethod
    def add_callbacks(self, app: Dash):
        pass


class OverheadDiv(ABC):
    def __init__(self, display_name: str, internal_name: str):
        self.display_name = display_name
        self.internal_name = internal_name

    @abstractmethod
    def get_html(self):
        pass

    @abstractmethod
    def add_callbacks(self, app: Dash):
        pass


def format_dcc_style(**kwargs) -> Dict[str, str]:
    """
    produces style formatting for dropdowns in my dash apps
    """
    dropdown_style = {}

    for key, value in kwargs.items():
        dropdown_style[key] = value

    return dropdown_style


def create_dropdown_from_pandas(data_: pd.DataFrame, col1: str, col2=None) -> List[Dict[str, str]]:
    """
    implementation of the dropdown list from the selection of days that are pulled
    """
    if col2 is None:
        return [{"label": data_.loc[i, col1], "value": data_.loc[i, col1]} for i in range(len(data_.index))]
    else:
        return [{"label": data_.loc[i, col1], "value": data_.loc[i, col2]} for i in range(len(data_.index))]


def create_dropdown_from_lists(label_list: list, value_list=None) -> List[Dict[str, str]]:
    """
    implementation of the dropdown list from the selection of days that are pulled
    """
    if value_list is None:
        return [{"label": label_list[i], "value": label_list[i]} for i in range(len(label_list))]
    else:
        return [{"label": label_list[i], "value": value_list[i]} for i in range(len(label_list))]


def title(text_: str) -> html:
    """
    dash implementation of a title
    """
    return html.H1(children=text_)


def body_text(text_: str) -> html:
    """
    body text for an app layout
    """
    return html.Div(children=text_)


def format_table_cols(column_list: list) -> List[Dict[str, str]]:
    """
    columns option for the dash data table implementation
    """
    return [{"name": col, "id": col} for col in column_list]


def format_options(options_list: list, key1="label", key2="value") -> List[Dict[str, str]]:
    """
    option list for dash formatting specifics
    """
    return [{key1: option, key2: option} for option in options_list]


def generic_graph_layout(title_: str) -> Dict[str, object]:
    """
    generic layout for a dash graph
    """
    return {"title": title_, "showlegend": True, "legend": {"x": 0, "y": 1.0},
            "margin": {"l": 40, "r": 0, "t": 40, "b": 30}}


def is_business_day(date: dt) -> bool:
    """
    checks whether a datetime is a business day
    """
    return bool(len(pd.bdate_range(date, date)))


def next_business_day(date_: dt, strip=True) -> dt.datetime:
    """
    determines the next business day after a given date
    """
    next_day = dt.datetime(date_.year, date_.month, date_.day) + dt.timedelta(days=1)

    if next_day.weekday() in holidays.WEEKEND or str(next_day) in holidays.US():
        return next_business_day(next_day)
    else:
        return dt.datetime(year=next_day.year, month=next_day.month, day=next_day.day) if strip else next_day


def last_business_day(date_: dt, strip=True) -> dt.datetime:
    """
    determines the last business day before a given date
    """

    last_day = dt.datetime(date_.year, date_.month, date_.day) - dt.timedelta(days=1)

    if last_day.weekday() in holidays.WEEKEND or str(last_day) in holidays.US():
        return last_business_day(last_day)
    else:
        return dt.datetime(year=last_day.year, month=last_day.month, day=last_day.day) if strip else last_day


if __name__ == "__main__":
    pass
