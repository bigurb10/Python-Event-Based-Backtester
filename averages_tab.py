"""

"""

from typing import List
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as d_t
from dash.dependencies import Input, Output
import plotly.graph_objects as go

from gui_support import DashboardTab
from backtesters import event_backtester as ebt


backtest_clicked = 0


class Averages(DashboardTab):

    def __init__(self, display_name: str, internal_name: str):
        super().__init__(display_name, internal_name)

    def get_html(self):
        return html.Div([
            dcc.Tab(label="Backtest Results",
                    children=[
                        dcc.Tabs([
                            dcc.Tab(label="Table", children=[
                                d_t.DataTable(id="averages_table", filter_action="native", sort_action="native")
                            ]),
                            dcc.Tab(label="Figure", children=[
                                dcc.Graph(id="averages_graph")
                            ])
                        ])
                    ])
        ])

    def add_callbacks(self, app: dash.Dash):
        @app.callback([Output(component_id="averages_table", component_property="data"),
                       Output(component_id="averages_table", component_property="columns")],
                      [Input(component_id="raw_data", component_property="data"),
                       Input(component_id="days_out", component_property="value"),
                       Input(component_id="averages", component_property="value")])
        def update_average_table(data: List[dict], days_out: List[int], averages: List[object]):
            data = pd.DataFrame(data)
            if not data.empty:
                data["date"] = pd.to_datetime(data["date"])
                data = ebt.derive_average_data(data, days_out, averages)
                for column in data.columns[1:]:
                    data[column] = data[column].map('%{:,.4f}'.format)
                data.columns = ["Type"] + [f"{x.split('_')[1]} Day Later %" for x in data.columns[1:]]
                return [data.to_dict("records"), [{"name": i, "id": i} for i in data.columns]]
            else:
                return [[], []]

        @app.callback(Output(component_id="averages_graph", component_property="figure"),
                      [Input(component_id="raw_data", component_property="data"),
                       Input(component_id="days_out", component_property="value"),
                       Input(component_id="averages", component_property="value")])
        def update_average_figure(data: List[dict], days_out: List[int], averages: List[object]):
            data = pd.DataFrame(data)
            if not data.empty:
                data["date"] = pd.to_datetime(data["date"])
                data = ebt.derive_average_data(data, days_out, averages).T
                data.columns = data[data.index == "type"].values.tolist()[0]
                data.drop(["type"], inplace=True)
                fig = go.Figure()
                for column in data.columns:
                    fig.add_trace(go.Scatter(name=column, x=data.index, y=data[column]))
                fig.update_layout(title="Returns by Days in Future by # of Years Back", xaxis_title="% Returns x Days in The Future",
                                  yaxis_title="Percent Return", legend_title="Data Splits", yaxis_tickformat="%")
                return fig
            else:
                return go.Figure()


if __name__ == "__main__":
    pass
