import pandas as pd
from dash import Dash, Input, Output, dcc, html
import os
import sys

# Add the utils folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils/")))

from utilities import get_data_frame

frame = get_data_frame()
countries = frame['Country'].unique()

def get_frame_by_wine_name(frame, name):
    df = pd.DataFrame(frame)
    df = df[df['Name'] == name]
    return df

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
wines = df_of_one_region['Name'].unique()
regions = df_of_one_region['Region'].str.split(' / ').apply(lambda x: x[1] if len(x) > 1 else None).unique()

df_of_one_region_one_wine_style = wine_style_selection_by_country_and_region(frame, countries[0], regions[0])
wine_styles = df_of_one_region_one_wine_style['Wine style'].unique()
wine_styles = [style for style in wine_styles if pd.notna(style)]

# Include Bootstrap styles
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Wine Analytics"

app.layout = html.Div(
    className="container mt-5",
    children=[
        html.Div(
            className="text-center mb-4",
            children=[
                html.P(children="🍷", className="fs-1"),
                html.H1(children="Wine Analytics", className="display-4 fw-bold"),
                html.P(
                    children="Analyze wine data across countries, regions, and wine styles.",
                    className="lead",
                ),
            ],
        ),
        html.Div(
            className="row mb-4",
            children=[
                html.Div(
                    className="col-md-4",
                    children=[
                        html.Label("Country", className="form-label fw-bold"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in countries
                            ],
                            value=countries[0],
                            clearable=False,
                            className="form-select",
                        ),
                    ],
                ),
                html.Div(
                    className="col-md-4",
                    children=[
                        html.Label("Region", className="form-label fw-bold"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region} for region in regions
                            ],
                            value=regions[0],
                            clearable=False,
                            className="form-select",
                        ),
                    ],
                ),
                html.Div(
                    className="col-md-4",
                    children=[
                        html.Label("Wine Style", className="form-label fw-bold"),
                        dcc.Dropdown(
                            id="wine-style-filter",
                            options=[
                                {"label": wine_style, "value": wine_style}
                                for wine_style in wine_styles
                            ],
                            value=wine_styles[0],
                            clearable=False,
                            className="form-select",
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-12",
                    children=[
                        dcc.Graph(
                            id="BTSA-chart",
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            children=[
                html.Div(children="Wine search in Country", className="menu-title"),
                dcc.Dropdown(
                    id="wine-search",
                    options=[
                        {"label": wine, "value": wine}
                        for wine in wines
                    ],
                    value=None,
                    searchable=True,
                    className="dropdown",
                ),
                html.Div(id='wine-search-output')
            ],
        ),

    #Single wine view starts 


    #Single wine view ends 

    ],

         

)

@app.callback(
    Output("wine-search", "options"),
    Input("country-filter", "value")
)
def update_region_options(selected_country):
    if selected_country:
        df_of_one_region = region_selection_by_country(frame, selected_country)
        wines = df_of_one_region['Name'].unique()
        return [{"label": wine, "value": wine} for wine in wines]
    return []

@app.callback(
    Output('wine-search-output', 'children'),
    Input('wine-search', 'value')
)
def update_wine_search_output(value):
    df = get_frame_by_wine_name(frame, value)
    return f'{df["Name"], df["Rating"], df["Number of Ratings"], df["Region"], df["Winery"], df["Wine style"], df["Alcohol content"], df["Grapes"], df["Food pairings"], df["Bold"], df["Tannin"], df["Sweet"], df["Acidic"]}'

@app.callback(
    Output("region-filter", "options"),
    Input("country-filter", "value")
)
def update_region_options(selected_country):
    if selected_country:
        df_of_one_region = region_selection_by_country(frame, selected_country)
        regions = df_of_one_region['Region'].str.split(' / ').apply(
            lambda x: x[1] if len(x) > 1 else None).unique()
        regions = [region for region in regions if pd.notna(region)]
        return [{"label": region, "value": region} for region in regions]
    return []

@app.callback(
    Output("wine-style-filter", "options"),
    Input("country-filter", "value"),
    Input("region-filter", "value")
)
def update_wine_style_options(country, region):
    if country:
        df_of_one_region_one_wine_style = wine_style_selection_by_country_and_region(frame, country, region)
        wine_styles = df_of_one_region_one_wine_style['Wine style'].unique()
        wine_styles = [style for style in wine_styles if pd.notna(style)]
        return [{"label": wine_style, "value": wine_style} for wine_style in wine_styles]
    return []

@app.callback(
    Output("region-filter", "value"),
    Output("wine-style-filter", "value"),
    Input("country-filter", "value")
)
def clear_wine_style_on_country_change(_):
    return None, None

@app.callback(
    Output("BTSA-chart", "figure"),
    Input("country-filter", "value"),
    Input("region-filter", "value"),
    Input("wine-style-filter", "value"),
)
def update_charts(country, region, wine_style):
    filtered_data = df_selection_by_country_and_region_and_wine_style(frame, country, region, wine_style)

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
    return BTSA_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)
