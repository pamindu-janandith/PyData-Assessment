import pandas as pd
from dash import Dash, Input, Output, dcc, html, callback
import glob, os
import plotly.graph_objs as go
import sys
sys.path.append("../utils/")

from utilities import get_data_frame

frame = get_data_frame()
countries = frame['Country'].unique()

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "PyData Assessment"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🍷", className="header-emoji"),
                html.H1(
                    children="Wine Analytics", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze the behavior of avocado prices and the number"
                        " of avocados sold in the US between 2015 and 2018"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in countries
                            ],
                            value="USA",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # html.Div(
                #     children=[
                #         html.Div(children="Type", className="menu-title"),
                #         dcc.Dropdown(
                #             id="type-filter",
                #             options=[
                #                 {
                #                     "label": avocado_type.title(),
                #                     "value": avocado_type,
                #                 }
                #                 for avocado_type in avocado_types
                #             ],
                #             value="organic",
                #             clearable=False,
                #             searchable=False,
                #             className="dropdown",
                #         ),
                #     ],
                # ),
                # html.Div(
                #     children=[
                #         html.Div(
                #             children="Date Range", className="menu-title"
                #         ),
                #         dcc.DatePickerRange(
                #             id="date-range",
                #             min_date_allowed=data["Date"].min().date(),
                #             max_date_allowed=data["Date"].max().date(),
                #             start_date=data["Date"].min().date(),
                #             end_date=data["Date"].max().date(),
                #         ),
                #     ]
                # ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="BTSA-chart",
                        
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Output("BTSA-chart", "figure"),
    Input("country-filter", "value"),
)
def update_charts(country):
    filtered_data = frame.query(
        "Country == @country"
    )
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Name"],
                "y": filtered_data["Price"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Wine Price",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    BTSA_chart_figure = {
        'data': [
            {'x': filtered_data['Name'], 'y': filtered_data['Bold'], 'type': 'bar', 'name': 'Bold'},
            {'x': filtered_data['Name'], 'y': filtered_data['Tannin'], 'type': 'bar', 'name': 'Tannin'},
            {'x': filtered_data['Name'], 'y': filtered_data['Sweet'], 'type': 'bar', 'name': 'Sweet'},
            {'x': filtered_data['Name'], 'y': filtered_data['Acidic'], 'type': 'bar', 'name': 'Acidic'},
        ],
        'layout': {
            'title': 'Wine Data Visualization'
        }
    }
    return price_chart_figure, BTSA_chart_figure

def get_app():
    return app

if __name__ == "__main__":
    app.run_server(debug=True)
