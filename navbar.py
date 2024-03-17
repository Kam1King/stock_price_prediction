
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
from dash import Input, Output, State, html
from datetime import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.express as px
import dash_auth as authi
from model import prediction
from sklearn.svm import SVR
from ft import about

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


app = dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])

auth = authi.BasicAuth(app,{"ketan":"1234"})


nav_item = dbc.NavItem(dbc.NavLink("ABOUT US ", href="#"))


dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("HOME"),
        dbc.DropdownMenuItem("FEATURE1"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("FEATURE2"),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)


default = dbc.NavbarSimple(
    children=[dropdown],
    brand="Default",
    brand_href="#",
    sticky="top",
    className="mb-5",
)

def get_stock_price_fig(df):
    
    fig = px.line(df,
                  x="Date",
                  y=["Close", "Open"],
                  title="Closing and Openning Price vs Date")

    return fig

def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
                     x="Date",
                     y="EWA_20",
                     title="Exponential Moving Average vs The Date")
    fig.update_traces(mode='lines+markers')
    return fig

logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("infostocks", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

app.layout = html.Div(
    [
    
                logo,
                dcc.Location(id='url', refresh=True, ),
                html.Div(id='page-content', children=[]),

                html.H1 ("Welcome to the infostock app.pvt.ltd", className="start"),

                html.P("Stock analysis and screening tool for investors in India.",className="temp"),
                
                html.Div([
                    html.P("Input stock code: ",className="temp1"),

                    html.Div([
                        dcc.Input(id="dropdown_tickers", type="text",className="temp2"),

                        html.Button("Submit", id='submit'
                        ),
                    ],
                            className="form")
                ],
                        className="input-place"),

                html.Div([
                    dcc.DatePickerRange(id='my-date-picker-range',
                                        min_date_allowed=dt(1995, 8, 5),
                                        max_date_allowed=dt.now(),
                                        initial_visible_month=dt.now(),
                                        end_date=dt.now().date()),
                ],
                         className="date"),
                
                html.Button("Indicators",className="indicators-btn",id="indicators"),

                
                html.Button("Stock Price", className="stock-btn", id="stock"),
                
                html.Div([
                dcc.Input(id="n_days",type="text",placeholder="Enter the number of days",className="temp3 "),

                html.Button("Forecast", className="forecast-btn", id="forecast"),
                        ],
                            className="form2"),
                


                html.Div(
            [
                html.Div(
                    [  # header
                        html.Img(id="logo"),
                        html.P(id="ticker")
                    ],
                    className="header"),

                html.Div(id="description", className="decription_ticker"),
                html.Div([], id="graphs-content"),
                html.Div([], id="main-content"),
                html.Div([], id="forecast-content")

            ],
            className="content"),
        html.Div([dcc.Link('ABOUT', href='/ft/about'),], className="row"),
        

    ],)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/ft/about':
        return about.card_main
    
@app.callback([
    Output("description", "children"),
    Output("logo", "src"),
    Output("ticker", "children"),
    Output("stock", "n_clicks"),
    Output("indicators", "n_clicks"),
    Output("forecast", "n_clicks")
], [Input("submit", "n_clicks")], [State("dropdown_tickers", "value")])

def update_data(n, val):  # inpur parameter(s)
    if n == None:
        return ".", "https://logopond.com/chgvisual/showcase/detail/81182.png", "INFOSTOCK", None, None, None
        # raise PreventUpdate
    else:
        if val == None:
            raise PreventUpdate
        else:
            ticker = yf.Ticker(val)
            inf = ticker.info
            df = pd.DataFrame().from_dict(inf, orient="index").T
            df[['logo_url', 'shortName', 'longBusinessSummary']]
            return df['longBusinessSummary'].values[0], df['logo_url'].values[
                0], df['shortName'].values[0], None, None, None

@app.callback([
    Output("graphs-content", "children"),
], [
    Input("stock", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def stock_price(n, start_date, end_date, val):
    if n == None:
        return [""]
        #raise PreventUpdate
    if val == None:
        raise PreventUpdate
    else:
        if start_date != None:
            df = yf.download(val, str(start_date), str(end_date))
        else:
            df = yf.download(val)

    df.reset_index(inplace=True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]

@app.callback([Output("main-content", "children")], [
    Input("indicators", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def indicators(n, start_date, end_date, val):
    if n == None:
        return [""]
    if val == None:
        return [""]

    if start_date == None:
        df_more = yf.download(val)
    else:
        df_more = yf.download(val, str(start_date), str(end_date))

    df_more.reset_index(inplace=True)
    fig = get_more(df_more)
    return [dcc.Graph(figure=fig)]

@app.callback([Output("forecast-content", "children")],
              [Input("forecast", "n_clicks")],
              [State("n_days", "value"),
               State("dropdown_tickers", "value")])
def forecast(n, n_days, val):
    if n == None:
        return [""]
    if val == None:
        raise PreventUpdate
    fig = prediction(val, int(n_days) + 1)
    return [dcc.Graph(figure=fig)]


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)