import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

BS = ["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"]

app = dash.Dash(__name__, external_stylesheets=BS)


app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ],
            align="start",
        ),
              dcc.Checklist(
                id='surf_trans',
                options=[
                    {'label':'Surface transmission', 'value': 'T'}
                ],
                value=['T'],
                labelStyle={'display': 'inline-block'}
            ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ],
            align="end",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), align="start"),
                dbc.Col(html.Div("One of three columns"), align="center"),
                dbc.Col(html.Div("One of three columns"), align="end"),
            ]
        ),
        dbc.Row(
            [
                html.H6("Change the value in the text box to see callbacks in action!"),
                html.Div(["Input: ",dcc.Input(id='my-input', value='initial value', type='text')]),
                html.Br(),
                html.Div(id='my-output'),
                        ]
        )
    
    ]
)

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value'),
    )
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)