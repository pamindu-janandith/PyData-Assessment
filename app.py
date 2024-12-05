import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Sample Data
wine_data = pd.DataFrame({
    "Country": ["Australia", "Chile", "France", "Italy", "New Zealand", "Portugal", "Spain", "USA"],
    "Wine Name": ["Wine A", "Wine B", "Wine C", "Wine D", "Wine E", "Wine F", "Wine G", "Wine H"],
    "Rating": [4.5, 4.0, 4.8, 4.7, 4.3, 4.1, 4.6, 4.2],
    "Number of Ratings": [100, 150, 200, 250, 80, 120, 180, 140],
    "Price": [25, 18, 30, 22, 28, 20, 24, 19],
    "Region": ["Region 1", "Region 2", "Region 3", "Region 4", "Region 5", "Region 6", "Region 7", "Region 8"],
    "Winery": ["Winery A", "Winery B", "Winery C", "Winery D", "Winery E", "Winery F", "Winery G", "Winery H"],
    "Wine Style": ["Style A", "Style B", "Style C", "Style D", "Style E", "Style F", "Style G", "Style H"],
    "Alcohol Content": [13.5, 12.0, 14.0, 13.0, 12.5, 13.2, 14.5, 13.8],
    "Grapes": ["Grape A", "Grape B", "Grape C", "Grape D", "Grape E", "Grape F", "Grape G", "Grape H"],
    "Food Pairing": ["Food 1", "Food 2", "Food 3", "Food 4", "Food 5", "Food 6", "Food 7", "Food 8"],
    "Bold": [4, 3, 5, 4, 3, 4, 5, 3],
    "Tannin": [3, 2, 4, 3, 2, 3, 4, 2],
    "Sweet": [2, 3, 1, 2, 3, 2, 1, 2],
    "Acidic": [3, 4, 2, 3, 4, 3, 2, 4]
})

# Create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div( 
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Analytics", href="/analytics", active="exact"),
            ],
            brand="Wine Dashboard",
            color="dark",
            dark=True,
        ), 
        style={"margin-bottom": "20px"}
    ),
    html.Div(id="page-content", style={"padding": "20px"}),
])

# Content Callback
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H3("Wine Overview", className="text-center"),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=px.bar(
                        wine_data,
                        x="Country",
                        y="Number of Ratings",
                        color="Rating",
                        title="Number of Ratings by Country",
                        labels={"Number of Ratings": "Ratings"},
                    )
                ), width=6),
                dbc.Col(dcc.Graph(
                    figure=px.pie(
                        wine_data,
                        values="Price",
                        names="Country",
                        title="Average Price Distribution by Country"
                    )
                ), width=6),
            ]),
        ])
    elif pathname == "/analytics":
        return html.Div([
            html.H3("Wine Analytics", className="text-center"),
            dbc.Row([
                dbc.Col([
                    html.Label("Select Country:"),
                    dcc.Dropdown(
                        id="country-filter",
                        options=[{"label": country, "value": country} for country in wine_data["Country"].unique()],
                        value="Australia",
                        clearable=False,
                    ),  
                ], width=4),  
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dcc.Graph(id="wine-rating-chart"), width=6),
                dbc.Col(dcc.Graph(id="wine-price-chart"), width=6),
            ]),
        ])
    return html.Div([
        html.H3("404: Page not found", className="text-center text-danger"),
    ])

# Callback for Analytics Page
@app.callback(
    [Output("wine-rating-chart", "figure"), Output("wine-price-chart", "figure")],
    Input("country-filter", "value")
)
def update_charts(selected_country):
    filtered_data = wine_data[wine_data["Country"] == selected_country]

    rating_chart = px.bar(
        filtered_data,
        x="Wine Name",
        y="Rating",
        title=f"Wine Ratings in {selected_country}",
        labels={"Rating": "Wine Rating"}
    )
    price_chart = px.bar(
        filtered_data,
        x="Wine Name",
        y="Price",
        title=f"Wine Prices in {selected_country}",
        labels={"Price": "Wine Price"}
    )
    return rating_chart, price_chart

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
