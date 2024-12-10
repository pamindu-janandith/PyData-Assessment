from dash import Dash, dcc, html, Input, Output
import pandas as pd
import os
import sys
import ast

# Add the utils folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils/")))

from utilities import get_data_frame

# Load the data
frame = get_data_frame()
countries = frame['Country'].unique()

def get_frame_by_wine_name(frame, name):
    df = pd.DataFrame(frame)
    df = df[df['Name'] == name]
    return df

def filter_by_country(frame, country):
    df = pd.DataFrame(frame)
    df = df[df['Country'] == country]
    return df

def filter_by_country_and_region(frame, country, region):
    df = pd.DataFrame(frame)
    df = df[df['Country'] == country]
    df = df[df['Region'].str.contains(region, na=False)]
    return df

def filter_by_country_and_region_and_wine_style(frame, country, region, wine_style):
    df = pd.DataFrame(frame)
    df = df[df['Country'] == country]
    df = df[df['Region'].str.contains(region, na=False)]
    df = df[df['Wine style'] == wine_style]
    return df

# Initialize data for the first dropdowns
df_of_one_country = filter_by_country(frame, countries[0])
wines = df_of_one_country['Name'].unique()

regions = df_of_one_country['Region'].str.split(' / ').apply(lambda x: x[1] if len(x) > 1 else None).unique()
df_of_one_country_and_one_region = filter_by_country_and_region(frame, countries[0], regions[0])

wine_styles = df_of_one_country_and_one_region['Wine style'].unique()
wine_styles = [style for style in wine_styles if pd.notna(style)]

# Dash app
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "🍷 Wine Dashboard"

# Layout
app.layout = html.Div(
    className="container mt-5",
    children=[
        html.Div(
            className="text-center mb-4",
            children=[
                html.H1("🍷 Wine Dashboard 🍷", className="display-4 fw-bold"),
                html.P("Analyze wine data and search for specific wines.", className="lead"),
            ],
        ),
        dcc.Tabs(
            id="tabs",
            value="analytics",
            children=[
                # Tab 1: Wine Analytics
                dcc.Tab(
                    label="Wine Analytics",
                    value="analytics",
                    children=[
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
                        dcc.Graph(id="BTSA-chart"),
                        html.Div(style={"height": "150px"})
                    ],
                ),
                # Tab 2: Search Wine
                dcc.Tab(
                    label="Search Wine",
                    value="search",
                    children=[
                        html.Div(
                            className="row mb-4",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    children=[
                                        html.Label("Country", className="form-label fw-bold"),
                                        dcc.Dropdown(
                                            id="country-filter-for-wine-search",
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
                                    className="col-md-6",
                                    children=[
                                        html.Label("Wine Search", className="form-label fw-bold"),
                                        dcc.Dropdown(
                                            id="wine-search",
                                            options=[{"label": wine, "value": wine} for wine in wines],
                                            value=None,
                                            searchable=True,
                                            className="form-select",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        #Single wine view starts 
                        
                            html.Div(
                                children=[
                                    html.H5(
                                        id = "wine-name",
                                        className="text-start mb-4",
                                        style={"fontFamily": "Cursive"}
                                    ),
                                    html.Div(
                                    children=[
                                        html.Img(
                                            id = "wine-img",
                                            className="img-fluid",
                                            style={
                                            "maxWidth": "200px",
                                            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
                                            }
                                        ),
                                        html.Div(
                                            children=[
                                                html.H6(className="text-start mt-4"),
                                                html.Div(
                                                    id = "food-pairings",
                                                    className="d-flex justify-content-start mt-3"
                                                ),
                                                html.P(
                                                    id = "wine-alcohol-content",
                                                    className="mt-4 mb-1 fw-bold"
                                                ),
                                                html.P(
                                                    id = "wine-winery",
                                                    className="fw-bold"
                                                )
                                            ],
                                            className="ms-4"
                                        )
                                    ],
                                    className="d-flex align-items-center"
                                    )
                                ],
                            className="p-4 bg-white rounded",
                            style={"border": "1px solid #ccc"}
                        ),
                        html.Div(style={"height": "150px"})
                    ],
                )
            ],
        ),
    ],
)

# Callbacks

# This is for the region-filter
@app.callback(
    Output("region-filter", "options"),
    Input("country-filter", "value")
)
def update_region_options(selected_country):
    if selected_country:
        df = filter_by_country(frame, selected_country)
        regions = df['Region'].str.split(' / ').apply(
            lambda x: x[1] if len(x) > 1 else None).unique()
        regions = [region for region in regions if pd.notna(region)]
        return [{"label": region, "value": region} for region in regions]
    return []

# This is for the wine-style-filter

@app.callback(
    Output("wine-style-filter", "options"),
    Input("country-filter", "value"),
    Input("region-filter", "value")
)
def update_wine_style_options(country, region):
    if country and region:
        df = filter_by_country_and_region(frame, country, region)
        wine_styles = df['Wine style'].unique()
        wine_styles = [style for style in wine_styles if pd.notna(style)]
        return [{"label": wine_style, "value": wine_style} for wine_style in wine_styles]
    return []

# This is for the Graph

@app.callback(
    Output("BTSA-chart", "figure"),
    Input("country-filter", "value"),
    Input("region-filter", "value"),
    Input("wine-style-filter", "value"),
)
def update_charts(country, region, wine_style):
    if not country or not region or not wine_style:
        return {}
    
    filtered_data = filter_by_country_and_region_and_wine_style(frame, country, region, wine_style)
    return {
        "data": [
            {"x": filtered_data["Name"], "y": filtered_data["Bold"], "type": "bar", "name": "Bold"},
            {"x": filtered_data["Name"], "y": filtered_data["Tannin"], "type": "bar", "name": "Tannin"},
            {"x": filtered_data["Name"], "y": filtered_data["Sweet"], "type": "bar", "name": "Sweet"},
            {"x": filtered_data["Name"], "y": filtered_data["Acidic"], "type": "bar", "name": "Acidic"},
        ],
        "layout": {"title": "Wine Data Visualization"},
    }


# Callbacks for the Second Tab

# For wine search filter

@app.callback(
    Output("wine-search", "options"),
    Input("country-filter-for-wine-search", "value")
)
def update_region_options(selected_country):
    if selected_country:
        df = filter_by_country(frame, selected_country)
        wines = df['Name'].unique()
        return [{"label": wine, "value": wine} for wine in wines]
    return []

# wine bottle img

@app.callback(
    Output("wine-img","src"),
    Input("wine-search", "value"),
    Input("country-filter-for-wine-search", "value")
)
def update_region_options(selected_country, wine):
    if selected_country and wine:
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzJBQ2Oo7u2kRd3oh_COy9MQL1lBkE54lumw&s"
    return ""

# For wine Details div

@app.callback(
    Output("wine-name", "children"),
    Output("food-pairings", "children"),
    Output("wine-alcohol-content", "children"),
    Output("wine-winery", "children"),
    Input("wine-search", "value")
)
def update_wine_search_output(value):
    wine_name=""
    food_pairings_div = []
    wine_alcohol_content=""
    wine_winery ="" 

    if value:
        df = get_frame_by_wine_name(frame, value)
        wine_name = df["Name"].iloc[0] if not df.empty else "Unknown"

        wine_food_pairings = df["Food pairings"].iloc[0] if not df.empty else []
        food_pairings_list = ast.literal_eval(wine_food_pairings)
        for food in food_pairings_list:
            food_pairings_div.append(
                html.Div(
                    children=[
                        html.Img(
                            src="https://via.placeholder.com/50",
                            className="rounded",
                            alt=str(food),
                            style={"width": "50px", "height": "50px"}
                        ),
                        html.P(
                            children=str(food),
                            className="text-center mt-2 small"
                        )
                    ],
                    className="d-inline-block text-center me-3"
                )
            )
            
        wine_alcohol_content = f"Alcohol content: {df['Alcohol content'].iloc[0]}" if not df.empty else ""
        wine_winery = df["Winery"].iloc[0] if not df.empty else "Unknown Winery"
        
    return wine_name,food_pairings_div, wine_alcohol_content, wine_winery



if __name__ == "__main__":
    app.run_server(debug=True)
