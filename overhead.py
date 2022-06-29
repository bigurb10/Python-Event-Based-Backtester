"""

"""
import base64
import pandas as pd
import io
from typing import Dict, List
import dash_table
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import event_backtester as ebt
import gui_support as gen


check_clicked = 0
DAYS_OUT_LIST = [1, 2, 3, 4, 5, 20, 40, 60, 80, 120, 240]
DAYS_OUT_OPTIONS = [{"label": str(x), "value": x} for x in DAYS_OUT_LIST]

AVERAGES_LIST = [1, 5, 10, 20, "ALL"]
AVERAGES_OPTIONS = [{"label": str(x), "value": x} for x in AVERAGES_LIST]

UPLOAD_DEFAULTS = {
    "width": "25%",
    "height": "60px",
    "lineHeight": "60px",
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "borderRadius": "5px",
    "textAlign": "center",
    "margin": "10px"
}


class Overhead(gen.OverheadDiv):
    """

    """

    def __init__(self, display_name: str, internal_name: str):
        super().__init__(display_name, internal_name)

    def get_html(self):
        return html.Div(
            id="HelloWorld",
            children=[
                html.Label("Days Out to Show: "),
                dcc.Checklist(id="days_out", value=DAYS_OUT_LIST, options=DAYS_OUT_OPTIONS, labelStyle={"display": "inline-block"}),
                html.Label("Averages To Show (In Years): "),
                dcc.Checklist(id="averages", value=AVERAGES_LIST, options=AVERAGES_OPTIONS, labelStyle={"display": "inline-block"}),
                html.Label("Notional vs. Percentage: "),
                dcc.RadioItems(id="notional_percent", value="percent", options=[{"label": "Percent", "value": "percent"}, {"label": "Notional", "value": "notional"}], labelStyle={"display": "inline-block"}),
                html.Button("Refresh Backtest", id="refresh_backtest"),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                    style=UPLOAD_DEFAULTS
                ),
                html.Div([dash_table.DataTable(id="raw_data")], style={"display": "none"})
            ]
        )

    def add_callbacks(self, app: dash.Dash):
        @app.callback([Output("raw_data", "data"), Output("raw_data", "columns")],
                      [Input("refresh_backtest", "n_clicks"), Input("upload-data", "contents"), Input("days_out", "value")])
        def update_output(button_clicks: int, list_of_contents, days_out):
            global check_clicked
            if (button_clicks is not None) and (button_clicks > check_clicked):
                check_clicked += 1
                return parse_contents(list_of_contents, days_out)
            else:
                return [[], []]


def parse_contents(contents, days_out):
    """

    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        df["date"] = pd.to_datetime(df["date"])
        df = ebt.derive_backtest_results(df, days_out)
        df.sort_values(by="date", ascending=True, inplace=True)
    except Exception as e:
        return dash_table.DataTable([{}])
    return [df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]]


if __name__ == "__main__":
    pass
