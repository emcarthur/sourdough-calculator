#https://dash-bootstrap-components.opensource.faculty.ai/docs
#https://dash.plotly.com/dash-core-components/input
#https://github.com/dcbark01/DashAppTemplate
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

standalone_radio_check = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Checkbox(
                    id="standalone-checkbox", className="form-check-input"
                ),
                dbc.Label(
                    "This is a checkbox",
                    html_for="standalone-checkbox",
                    className="form-check-label",
                ),
            ],
            check=True,
        ),
        dbc.FormGroup(
            [
                dbc.RadioButton(
                    id="standalone-radio", className="form-check-input"
                ),
                dbc.Label(
                    "This is a radio button",
                    html_for="standalone-radio",
                    className="form-check-label",
                ),
            ],
            check=True,
        ),
        html.Br(),
        html.P(id="standalone-radio-check-output"),
    ]
)


@app.callback(
    Output("standalone-radio-check-output", "children"),
    [
        Input("standalone-checkbox", "checked"),
        Input("standalone-radio", "checked"),
    ],
)
def on_form_change(checkbox_checked, radio_checked):
    if checkbox_checked and radio_checked:
        return "Both checked."
    elif checkbox_checked or radio_checked:
        return "One checked."
    else:
        return "None checked."

########## Jumbotron ########
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H2(
                    [
                    "Sourdough Calculator",
                    html.Small(html.Small(" by Evonne McArthur"),className="text-muted")
                    ],
                ),
                html.P("Generate and evaluate the properties of custom Sourdough recipes. Compare your recipe to others!",
                className="lead",
                )
            ],
            fluid=True,
        )
    ],
    fluid=True,
)
####### input group #######

levain_grams = dbc.InputGroup(
            [
                dbc.Input(value="100", type="number", step=1,min=0,style={'backgroundColor': '#b3e0af'}),
                dbc.InputGroupAddon("g", addon_type="append"),
            ]
        )
levain_percent = dbc.InputGroup(
            [
                dbc.Input(value="20", type="number", step=1,min=0,max=100,style={'backgroundColor': '#b8c1e6'}),
                dbc.InputGroupAddon("%", addon_type="append"),
            ]
        )
#### Tooltip #####

levain_tooltip = html.Div(
    [
        html.P(
            html.Span(
                    "Levain",
                    id="tooltip-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                ),
            ),
            dbc.Tooltip(
            "Mix of water, flour, and natural yeast (starter). Fermented until lively.",
            target="tooltip-target",
            ),
    ]
)

######### Table #########

table_header = [
    html.Thead(html.Tr([html.Th("Ingredients"), html.Th("Amount(g)"),html.Th("Bakers Percentage of ADDED flour"), html.Th("Bakers Percentage of ALL flour"), html.Th("True Percentage by weight")]))
]

levain_row = html.Tr([html.Td(levain_tooltip),html.Td(levain_grams), html.Td(levain_percent), html.Td("20 %"),  html.Td("10.4 %")])
flour_row = html.Tr([html.Td("Added Flour"),html.Td(levain_grams), html.Td(levain_percent), html.Td("20 %"),  html.Td("10.4 %")])
water_row = html.Tr([html.Td("Added Water"),html.Td(levain_grams), html.Td(levain_percent), html.Td("20 %"),  html.Td("10.4 %")])
salt_row = html.Tr([html.Td("Salt"),html.Td(levain_grams), html.Td(levain_percent), html.Td("20 %"),  html.Td("10.4 %")])
total_row = html.Tr([html.Td("Total dough weight"), html.Td("500", style={'borderTop': 'double'})])
table_body = [html.Tbody([levain_row, flour_row, water_row, salt_row, total_row])]

table = dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True)

######## Layout and display #########
app.layout = dbc.Container(
    [
        jumbotron,
        html.P(
            "Edit the green boxes to enter a custom recipe in grams and generate bakers percentages and statistics (hydration, etc) or edit the blue boxes to have a recipe generated for you based on your desired loaf weight and hydration."
        ),
        table
    ]
)

if __name__ == "__main__":
    app.run_server()
