from turtle import width
import dash

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

df = px.data.gapminder()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

card_main = dbc.Card(
    [
        dbc.CardImg(src="/assets/info", top=True, bottom=False,
                    title="Image by ketan", alt=''),

        dbc.CardBody(
            [
                html.H4("About US", className="card-title",style={"align-items": "center;"}),
                html.P("Infostock was created by Final year students of MIT-ADT University as a part of final year project"),
                html.P("Under the guidence of the Prof.Abhishek Das"),
                html.H6("CONTACT US", className="card-subtitle"),
                html.P(
                    "",
                    className="card-text",
                ),
                
            ]
        ),
    ],
    color="dark",   
    inverse=True,   
    outline=False,
      
)






app.layout = html.Div([
    
    dbc.Row([dbc.Col(card_main, width=12)])
    
,])



if __name__ == "__main__":
    app.run_server(debug=True)
    
    