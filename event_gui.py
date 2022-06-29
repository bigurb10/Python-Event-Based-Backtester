"""
supports implementation of portfolio analytics for options trading accounts
"""

from typing import List
import dash
import dash_html_components as html
import dash_core_components as dcc

from gui import gui_support as gen
from overhead import Overhead
from backtest_results_tab import BackTestResults
from averages_tab import Averages
DEFAULT_DATE_FORMAT = "%Y-%m-%d"


def create_app(overhead_content: gen.OverheadDiv, tab_content: List[gen.DashboardTab]):
    application = dash.Dash(__name__, external_stylesheets=gen.EXTERNAL_STYLESHEETS)
    tab_components = [dcc.Tab(label=tab.display_name, value=tab.internal_name, children=tab.get_html()) for tab in
                      tab_content]
    application.layout = html.Div(
        style={"display": "flex", "flex-direction": "column"},
        children=[
            gen.title("Event Backtester"),
            overhead_content.get_html(),
            dcc.Tabs(
                id="main_tab_content",
                children=tab_components
            )
        ])

    overhead_content.add_callbacks(application)
    for tab in tab_content:
        tab.add_callbacks(application)

    return application


if __name__ == '__main__':
    overhead = Overhead("Overhead", "overhead")
    tabs = [
        BackTestResults("Backtest Results", "backtest_results"),
        Averages("Averaged Results", "averaged_results")
    ]

    app = create_app(overhead, tabs)
    app.run_server(debug=True, port=8000)

if __name__ == '__main__':
    pass
