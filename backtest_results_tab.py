"""

"""

from typing import Tuple, List
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as d_t
from dash.dependencies import Input, Output

from gui_support import DashboardTab
import event_backtester as ebt


backtest_clicked = 0


class BackTestResults(DashboardTab):

    def __init__(self, display_name: str, internal_name: str):
        super().__init__(display_name, internal_name)

    def get_html(self):
        return html.Div([
            dcc.Tab(label="Backtest Results",
                    children=[
                        d_t.DataTable(id="backtest_table", filter_action="native", sort_action="native")
                    ])
        ])

    def add_callbacks(self, app: dash.Dash):
        @app.callback([Output(component_id="backtest_table", component_property="data"),
                       Output(component_id="backtest_table", component_property="columns")],
                      [Input(component_id="raw_data", component_property="data"),
                       Input(component_id="days_out", component_property="value")])
        def update_backtest_table(data: List[dict], days_out: List[int]):
            data = pd.DataFrame(data)
            if not data.empty:
                data["date"] = pd.to_datetime(data["date"])
                data = ebt.return_signal_days(data, days_out)
                data["date"] = data["date"].dt.strftime('%m-%d-%Y')
                for column in data.columns[1:]:
                    data[column] = data[column].map('%{:,.4f}'.format)
                data.columns = ["date"] + [f"{x.split('_')[1]} Day Later %" for x in data.columns[1:]]
                return [data.to_dict("records"), [{"name": i, "id": i} for i in data.columns]]
            else:
                return [[], []]


if __name__ == "__main__":
    pass
