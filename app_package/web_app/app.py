import pandas as pd
from dash import Dash, Input, Output, dcc, html, callback
import glob, os
import plotly.graph_objs as go
import sys
sys.path.append("../utils/")

from utilities import get_data_frame

frame = get_data_frame()
countries = frame['Country'].unique()

def region_selection_by_country(frame, country):
    df = pd.DataFrame(frame)
    df = df[df['Country'] == country]
    return df

def wine_style_selection_by_country_and_region(frame, country, region):
    df = pd.DataFrame(frame)
    df = df[df['Country'] == country]
    df = df[df['Region'].str.contains(region, na=False)]
    return df

def df_selection_by_country_and_region_and_wine_style(frame, country, region, wine_style):
    df = pd.DataFrame(frame)
    df = df[df['Country'] == country]
    df = df[df['Region'].str.contains(region, na=False)]
    df = df[df['Wine style'] == wine_style]
    return df

df_of_one_region = region_selection_by_country(frame, countries[0])
regions = df_of_one_region['Region'].str.split(' / ').apply(lambda x: x[1] if len(x) > 1 else None).unique()

df_of_one_region_one_wine_style = wine_style_selection_by_country_and_region(frame, countries[0], regions[0])
wine_styles = df_of_one_region_one_wine_style['Wine style'].unique()
wine_styles = [style for style in wine_styles if pd.notna(style)]

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
                                {
                                    "label": country, 
                                    "value": country
                                }
                                for country in countries
                            ],
                            value=countries[0],
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {
                                    "label": region,
                                    "value": region,
                                }
                                for region in regions
                            ],
                            value = regions[0],
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Wine Style", className="menu-title"),
                        dcc.Dropdown(
                            id="wine-style-filter",
                            options=[
                                {
                                    "label": wine_style,
                                    "value": wine_style,
                                }
                                for wine_style in wine_styles
                            ],
                            value = wine_styles[0],
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),

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
                # html.Div(
                #     children=dcc.Graph(
                #         id="price-chart",
                #         config={"displayModeBar": False},
                #     ),
                #     className="card",
                # ),
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
    Output("region-filter", "options"),
    Input("country-filter", "value")
)
def update_region_options(selected_country):
    if selected_country:
        df_of_one_region = region_selection_by_country(frame, selected_country)
        regions = df_of_one_region['Region'].str.split(' / ').apply(lambda x: x[1] if len(x) > 1 else None).unique()
        regions = [region for region in regions if pd.notna(region)]
        return [{"label": region, "value": region} for region in regions]
    return []

@app.callback(
    Output("wine-style-filter", "options"),
    Input("country-filter", "value"),
    Input("region-filter", "value")
)
def update_wine_style_options(country, region ):
    if country:
        df_of_one_region_one_wine_style = wine_style_selection_by_country_and_region(frame, country, region)
        wine_styles = df_of_one_region_one_wine_style['Wine style'].unique()
        wine_styles = [style for style in wine_styles if pd.notna(style)]
        return [{"label": wine_style, "value": wine_style} for wine_style in wine_styles]
    return []

# Callback to clear wine style dropdown when country is changed
@app.callback(
    Output("region-filter", "value"),
    Output("wine-style-filter", "value"),
    Input("country-filter", "value")
)
def clear_wine_style_on_country_change(_):
    return None, None

@app.callback(
    # Output("price-chart", "figure"),
    Output("BTSA-chart", "figure"),
    Input("country-filter", "value"),
    Input("region-filter", "value"),
    Input("wine-style-filter", "value"),
)
def update_charts(country, region, wine_style):
    # filtered_data = frame.query(
    #     "Country == @country"
    # )
    filtered_data = df_selection_by_country_and_region_and_wine_style(frame, country, region, wine_style)

    # price_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["Name"],
    #             "y": filtered_data["Price"],
    #             "type": "lines",
    #             "hovertemplate": "$%{y:.2f}<extra></extra>",
    #         },
    #     ],
    #     "layout": {
    #         "title": {
    #             "text": "Wine Price",
    #             "x": 0.05,
    #             "xanchor": "left",
    #         },
    #         "xaxis": {"fixedrange": True},
    #         "yaxis": {"tickprefix": "$", "fixedrange": True},
    #         "colorway": ["#17B897"],
    #     },
    # }

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
    return  BTSA_chart_figure #, price_chart_figure

def get_app():
    return app

if __name__ == "__main__":
    app.run_server(debug=True)
