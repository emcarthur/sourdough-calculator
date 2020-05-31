#https://dash-bootstrap-components.opensource.faculty.ai/docs
#https://dash.plotly.com/dash-core-components/input
#https://github.com/dcbark01/DashAppTemplate
#http://yaaics.blogspot.com/2019/03/circular-references-in-plotlydash.html
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
from dash.exceptions import PreventUpdate


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df = pd.DataFrame({'Ingredients': ["Levain", "AddedFlour","AddedWater","Salt"], 'Grams': [100, 500,350,10], 'BakersPercentAdded': [0.2,1,.7,.02],'BakersPercentAll':[np.nan, .931, .621, .018]})
df.index = df["Ingredients"]
levain_hydration = 1
totalDough_hydration = np.round(100*(df.loc["AddedWater","Grams"] + df.loc["Levain","Grams"]*(levain_hydration/(1+levain_hydration)))/(df.loc["AddedFlour","Grams"] + (df.loc["Levain","Grams"]/(1+levain_hydration))),2)


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

####### input group #######

levain_hydration_input = dbc.InputGroup(
            [
                dbc.Input(id='levain_hydration',type="number",value=100, min=0, debounce = True, max=100, step="any"),
                dbc.InputGroupAddon("% Hydration", addon_type="append"),
            ], size="sm", style={"margin-top": "-15px"}
        )

levain_grams = dbc.InputGroup(
            [
                dbc.Input(id='levain_grams',type="number",value=df.loc["Levain","Grams"], min=0, debounce = True, step="any", style={'backgroundColor': '#c1e6bd'}),
                dbc.InputGroupAddon("g", addon_type="append"),
            ]
        )

addedFlour_grams = dbc.InputGroup(
            [
                dbc.Input(id='addedFlour_grams',value=df.loc["AddedFlour","Grams"], type="number", min=0, debounce = True, step="any", style={'backgroundColor': '#c1e6bd'}),
                dbc.InputGroupAddon("g", addon_type="append"),
            ]
        )

addedWater_grams = dbc.InputGroup(
            [
                dbc.Input(id='addedWater_grams',value=df.loc["AddedWater","Grams"], type="number", min=0, debounce = True, step="any", style={'backgroundColor': '#c1e6bd'}),
                dbc.InputGroupAddon("g", addon_type="append"),
            ]
        )

salt_grams = dbc.InputGroup(
            [
                dbc.Input(id='salt_grams',value=df.loc["Salt","Grams"], type="number", min=0, debounce = True, step="any", style={'backgroundColor': '#c1e6bd'}),
                dbc.InputGroupAddon("g", addon_type="append"),
            ]
        )

levain_BakersPercentAdded = dbc.InputGroup(
            [
                dbc.Input(id='levain_BakersPercentAdded', value=100*df.loc["Levain","BakersPercentAdded"],type="number", debounce=True, min=0,max=100, step="any", style={'backgroundColor': '#cddaf6'}),
                dbc.InputGroupAddon("%", addon_type="append"),
            ]
        )

salt_BakersPercentAll = dbc.InputGroup(
            [
                dbc.Input(id='salt_BakersPercentAll', type="number", value=np.round(100*df.loc["Salt","BakersPercentAll"],2),debounce=True, min=0,max=100, step="any", style={'backgroundColor': '#cddaf6'}),
                dbc.InputGroupAddon("%", addon_type="append"),
            ]
        )

totalDough_grams = dbc.InputGroup(
            [
                dbc.Input(id='totalDough_grams', type="number", value = 960, debounce=True, min=0, step="any", style={'backgroundColor': '#cddaf6'}),
                dbc.InputGroupAddon("g", addon_type="append"),
            ]
        )

totalDough_hydration = dbc.InputGroup(
            [
                dbc.Input(id='totalDough_hydration', value = totalDough_hydration, type="number", debounce=True, min=0,max=100, step="any", style={'backgroundColor': '#cddaf6'}),
                dbc.InputGroupAddon("%", addon_type="append"),
            ]
        )

######### Table #########

table_header = [
    html.Thead(html.Tr([html.Th("Ingredients"), html.Th("Amount(g)"),html.Th("Bakers Percentage of ADDED flour"), html.Th("Bakers Percentage of ALL flour")]))
]

levain_row = html.Tr([html.Th([levain_tooltip,levain_hydration_input]),html.Td(levain_grams), html.Td(levain_BakersPercentAdded), html.Td("NA")])
flour_row = html.Tr([html.Th("Added Flour"),html.Td(addedFlour_grams), html.Td(str(np.round(100*df.loc["AddedFlour","BakersPercentAdded"],1)) + " %",id = 'addedFlour_BakersPercentAdded'), html.Td(str(np.round(100*df.loc["AddedFlour","BakersPercentAll"],1)) + " %",id ='addedFlour_BakersPercentAll')])
water_row = html.Tr([html.Th("Added Water"),html.Td(addedWater_grams), html.Td(str(np.round(100*df.loc["AddedWater","BakersPercentAdded"],1)) + " %",id = 'addedWater_BakersPercentAdded'), html.Td(str(np.round(100*df.loc["AddedWater","BakersPercentAll"],1)) + " %",id = 'addedWater_BakersPercentAll')])
salt_row = html.Tr([html.Th("Salt"),html.Td(salt_grams), html.Td(str(np.round(100*df.loc["Salt","BakersPercentAdded"],1)) + " %",id = 'salt_BakersPercentAdded'), html.Td(salt_BakersPercentAll)])
total_row = html.Tr([html.Th("Total dough weight", style={'borderTopWidth': '3px'}), html.Td(totalDough_grams, style={'borderTopWidth': '3px'})])
table_body = [html.Tbody([levain_row, flour_row, water_row, salt_row, total_row])]

table = dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True)

hydration_row = html.Tr([html.Th("Total dough hydration"),html.Th(totalDough_hydration)])
trad_hydration_row = html.Tr([html.Th("\"Traditional\" dough hydration"),html.Th(id = "trad_hydration", style={"fontWeight":"normal"})])

hydration_table = dbc.Table(html.Tbody([hydration_row, trad_hydration_row]),bordered=True,  hover=True)

##### List of directions #####

welcome_directions = html.Div(
    [
        html.P([
                u"\u2022 To generate a custom recipe in grams from a desired hydration and dough weight, edit the ",
                html.Span("green",style={"color": "#68c15e" , "fontWeight":"bold" }),
                " boxes."
            ]),
            html.P([
                u"\u2022 To evaluate the bakers percentages and hydration of a custom recipe, edit the ",
                html.Span("blue",style={"color": "#86a8f0" , "fontWeight":"bold" }),
                " boxes in grams."
                ] ,style={"margin-top": "-20px"}
            ),
            html.P([
                u"\u2022 To evaluate the protein content and dough stickiness, edit the ",
                html.Span("gold",style={"color": "#b89a26" , "fontWeight":"bold" }),
                " boxes with flour types."
            ] ,style={"margin-top": "-20px"}),
            html.P([
                u"\u2022 Hover over any ",
                html.Span("underlined",style={"textDecoration": "underline" }),
                " text to read more details."
            ] ,style={"margin-top": "-20px"})

    ]
)

######## call backs ############3

@app.callback(
    [Output('totalDough_grams', 'value'),
    Output('totalDough_hydration','value'),
    Output('levain_BakersPercentAdded', 'value'),
    Output('addedFlour_BakersPercentAdded', 'children'),
    Output('addedWater_BakersPercentAdded', 'children'),
    Output('salt_BakersPercentAdded', 'children'),
    Output('addedFlour_BakersPercentAll', 'children'),
    Output('addedWater_BakersPercentAll', 'children'),
    Output('salt_BakersPercentAll', 'value'),
    Output('trad_hydration','children')
    ],
    [Input('levain_grams', 'value'),
    Input('addedFlour_grams', 'value'),
    Input('addedWater_grams', 'value'),
    Input('salt_grams','value'),
    Input('levain_hydration','value')]

)
def update_table_inputInGrams(levain_grams, addedFlour_grams, addedWater_grams, salt_grams,levain_hydration_input):
    levain_hydration = levain_hydration_input/100

    df.loc["Levain","Grams"] = levain_grams
    df.loc["AddedFlour","Grams"] = addedFlour_grams
    df.loc["AddedWater","Grams"] = addedWater_grams
    df.loc["Salt","Grams"] = salt_grams
    df[["BakersPercentAdded"]] = df[["Grams"]] / df.loc["AddedFlour","Grams"]
    df[["BakersPercentAll"]] = df[["Grams"]] / (df.loc["AddedFlour","Grams"] + (df.loc["Levain","Grams"]/(1+levain_hydration)))

    totalDough_grams =  np.round(levain_grams + addedFlour_grams + addedWater_grams + salt_grams,1)

    totalDough_hydration = np.round(100*(df.loc["AddedWater","Grams"] + df.loc["Levain","Grams"]*(levain_hydration/(1+levain_hydration)))/(df.loc["AddedFlour","Grams"] + (df.loc["Levain","Grams"]/(1+levain_hydration))),2)
    trad_hydration = str(np.round(100*df.loc["AddedWater","Grams"]/df.loc["AddedFlour","Grams"],2)) + " %"
    levain_BakersPercentAdded = np.round(100*df.loc["Levain","BakersPercentAdded"],1)
    addedFlour_BakersPercentAdded = str(np.round(100*df.loc["AddedFlour","BakersPercentAdded"],1)) + " %"
    addedWater_BakersPercentAdded = str(np.round(100*df.loc["AddedWater","BakersPercentAdded"],1)) + " %"
    salt_BakersPercentAdded = str(np.round(100*df.loc["Salt","BakersPercentAdded"],2)) + " %"
    addedFlour_BakersPercentAll = str(np.round(100*df.loc["AddedFlour","BakersPercentAll"],1)) + " %"
    addedWater_BakersPercentAll = str(np.round(100*df.loc["AddedWater","BakersPercentAll"],1)) + " %"
    salt_BakersPercentAll = np.round(100*df.loc["Salt","BakersPercentAll"],2)
    return totalDough_grams, totalDough_hydration, levain_BakersPercentAdded, addedFlour_BakersPercentAdded, addedWater_BakersPercentAdded, salt_BakersPercentAdded, addedFlour_BakersPercentAll, addedWater_BakersPercentAll, salt_BakersPercentAll, trad_hydration

@app.callback(
    Output(component_id='loop_breaker_container', component_property='children'),
    [Input('totalDough_grams', 'value'),
    Input('totalDough_hydration','value'),
    Input('levain_BakersPercentAdded', 'value'),
    Input('salt_BakersPercentAll', 'value')
    ]
)
def update_table_inputInPercent(totalDough_grams,totalDough_hydration, levain_BakersPercentAdded, salt_BakersPercentAll):
    df.loc["AddedFlour","Grams"] = ((levain_hydration + 1)*totalDough_grams)/(((levain_BakersPercentAdded/100) + levain_hydration + 1)*((salt_BakersPercentAll/100) + (totalDough_hydration/100) + 1))
    df.loc["Levain","Grams"] = levain_BakersPercentAdded/100 * df.loc["AddedFlour","Grams"]
    df.loc["Salt","Grams"] = (df.loc["AddedFlour","Grams"]+(df.loc["Levain","Grams"]*(1/(1+levain_hydration))))*salt_BakersPercentAll/100
    df.loc["AddedWater","Grams"] = totalDough_grams - df.loc["Levain","Grams"] - df.loc["AddedFlour","Grams"] - df.loc["Salt","Grams"]

    df[["BakersPercentAdded"]] = df[["Grams"]] / df.loc["AddedFlour","Grams"]
    df[["BakersPercentAll"]] = df[["Grams"]] / (df.loc["AddedFlour","Grams"] + (df.loc["Levain","Grams"]/(1+levain_hydration)))

    levain_grams = df.loc["Levain","Grams"]
    addedFlour_grams = df.loc["AddedFlour","Grams"]
    addedWater_grams = df.loc["AddedWater","Grams"]
    salt_grams = df.loc["Salt","Grams"]

    addedFlour_BakersPercentAdded = 100*df.loc["AddedFlour","BakersPercentAdded"]
    addedWater_BakersPercentAdded = 100*df.loc["AddedWater","BakersPercentAdded"]
    salt_BakersPercentAdded = 100*df.loc["Salt","BakersPercentAdded"]
    addedFlour_BakersPercentAll = 100*df.loc["AddedFlour","BakersPercentAll"]
    addedWater_BakersPercentAll = 100*df.loc["AddedWater","BakersPercentAll"]

    return [html.Div(id='loop_breaker', children=[np.round(levain_grams,1), np.round(addedFlour_grams,1), np.round(addedWater_grams,1), np.round(salt_grams,1)])]

@app.callback([Output('levain_grams', 'value'),
    Output('addedFlour_grams', 'value'),
    Output('addedWater_grams', 'value'),
    Output('salt_grams','value')],
    [Input('loop_breaker', 'children')])
def update_output(loop_breaker_content):
    return loop_breaker_content

######## Layout and display #########
app.layout = dbc.Container(
    [
        jumbotron,
        welcome_directions,
        dbc.Row([
            dbc.Col(table, width=12,lg=8),
            dbc.Col(hydration_table, width=12,lg=4)
        ]),
        html.Div(id='loop_breaker_container',style={'display':'none'})
#        dcc.Input(id='my-id', value='initial value', type='number'),
        #html.Div(id='my-div')
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
