import dash_bootstrap_components as dbc
from dash import html

def create_sidebar():
    sidebar = html.Div(
        [
            html.H2("Dashboard", className="display-4"),
            html.Hr(),
            html.P("Navigation Menu", className="lead"),
            dbc.Nav(
                [
                    dbc.NavLink("Overview", href="/", active="exact"),
                    dbc.NavLink("Analytics", href="/analytics", active="exact"),
                    dbc.NavLink("Reports", href="/reports", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "18rem",
            "padding": "2rem 1rem",
            "background-color": "#f8f9fa",
        },
    )
    return sidebar
