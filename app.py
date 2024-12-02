import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Sample data
df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Values": [10, 20, 15, 25]
})

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Responsive Dashboard", className="text-center mt-4 mb-4"))
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select a category:"),
                        dcc.Dropdown(
                            id="category-dropdown",
                            options=[
                                {"label": cat, "value": cat} for cat in df["Category"]
                            ],
                            value="A",
                            className="mb-3"
                        ),
                    ],
                    width=4,
                    className="p-2"
                ),
                dbc.Col(
                    dcc.Graph(id="bar-chart"),
                    width=8,
                    className="p-2"
                )
            ]
        ),
    ],
    fluid=True,
)

# Callback
@app.callback(
    Output("bar-chart", "figure"),
    Input("category-dropdown", "value")
)
def update_chart(selected_category):
    filtered_df = df[df["Category"] == selected_category]
    fig = px.bar(filtered_df, x="Category", y="Values", title=f"Values for {selected_category}")
    fig.update_layout(template="plotly_white")
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

