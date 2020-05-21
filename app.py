#https://dash-bootstrap-components.opensource.faculty.ai/docs
#https://dash.plotly.com/dash-core-components/input
#https://github.com/dcbark01/DashAppTemplate
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df = pd.DataFrame({'Ingredients': ["Levain", "AddedFlour","AddedWater","Salt"], 'Grams': [100, 500,350,10], 'BakersPercentAdded': [0.2,1,.7,.02],'BakersPercentAll':[np.nan, .931, .621, .018]})
df.index = df["Ingredients"]

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


levain_grams = dbc.InputGroup(
            [
                dbc.Input(id='levain_grams',value=df.loc["Levain","Grams"], type="number", min=0, debounce = True, step="any", style={'backgroundColor': '#c1e6bd'}),
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
            [ #value=100*np.round(df.loc["Levain","BakersPercentAdded"],3),
                dbc.Input(id='levain_BakersPercentAdded',value = 100*df.loc["Levain","BakersPercentAdded"], type="number", debounce=True, min=0,max=100, step="any", style={'backgroundColor': '#cddaf6'}),
                dbc.InputGroupAddon("%", addon_type="append"),
            ]
        )

######### Table #########

table_header = [
    html.Thead(html.Tr([html.Th("Ingredients"), html.Th("Amount(g)"),html.Th("Bakers Percentage of ADDED flour"), html.Th("Bakers Percentage of ALL flour"), html.Th("True Percentage by weight")]))
]

levain_row = html.Tr([html.Td(levain_tooltip),html.Td(levain_grams), html.Td(levain_BakersPercentAdded), html.Td("20 %"),  html.Td("10.4 %")])
flour_row = html.Tr([html.Td("Added Flour"),html.Td(addedFlour_grams), html.Td(id = 'addedFlour_BakersPercentAdded'), html.Td("20 %"),  html.Td("10.4 %")])
water_row = html.Tr([html.Td("Added Water"),html.Td(addedWater_grams), html.Td(id = 'addedWater_BakersPercentAdded'), html.Td("20 %"),  html.Td("10.4 %")])
salt_row = html.Tr([html.Td("Salt"),html.Td(salt_grams), html.Td(id = 'salt_BakersPercentAdded'), html.Td("20 %"),  html.Td("10.4 %")])
total_row = html.Tr([html.Td("Total dough weight", style={'borderTopWidth': '3px'}), html.Td(id="totalDough_grams", style={'borderTopWidth': '3px'})])
table_body = [html.Tbody([levain_row, flour_row, water_row, salt_row, total_row])]

table = dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True)

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

# @app.callback(
#     Output('levain_BakersPercentAdded', 'value'),
#     [Input('levain_grams', 'value')]
# )
# def update_levain_BakersPercentAdded(input_value):
#     df.loc["Levain","Grams"] = input_value
#     df.loc["Levain","BakersPercentAdded"] = df.loc["Levain","Grams"]/df.loc["AddedFlour","Grams"]
#     return 100*df.loc["Levain","BakersPercentAdded"]

@app.callback(
    Output('levain_grams', 'value'),
    [Input('levain_BakersPercentAdded', 'value')]
)
def update_levain_grams(input_value):
    df.loc["Levain","BakersPercentAdded"] = input_value/100
    df.loc["Levain","Grams"] = df.loc["Levain","BakersPercentAdded"]*df.loc["AddedFlour","Grams"]
    return df.loc["Levain","Grams"]

@app.callback(
    [Output('totalDough_grams', 'children'),
    Output('levain_BakersPercentAdded', 'value'),
    Output('addedFlour_BakersPercentAdded', 'children'),
    Output('addedWater_BakersPercentAdded', 'children'),
    Output('salt_BakersPercentAdded', 'children')
    ],
    [Input('levain_grams', 'value'),
    Input('addedFlour_grams', 'value'),
    Input('addedWater_grams', 'value'),
    Input('salt_grams','value')]
)
def input_grams(levain_grams, addedFlour_grams, addedWater_grams, salt_grams):
    df.loc["Levain","Grams"] = levain_grams
    df.loc["AddedFlour","Grams"] = addedFlour_grams
    df.loc["AddedWater","Grams"] = addedWater_grams
    df.loc["Salt","Grams"] = salt_grams
    df[["BakersPercentAdded"]] = df[["Grams"]] / df.loc["AddedFlour","Grams"]
    totalDough_grams = df[["Grams"]].sum()
    levain_BakersPercentAdded = 100*df.loc["Levain","BakersPercentAdded"]
    addedFlour_BakersPercentAdded = 100*df.loc["AddedFlour","BakersPercentAdded"]
    addedWater_BakersPercentAdded = 100*df.loc["AddedWater","BakersPercentAdded"]
    salt_BakersPercentAdded = 100*df.loc["Salt","BakersPercentAdded"]
    return totalDough_grams, levain_BakersPercentAdded, addedFlour_BakersPercentAdded, addedWater_BakersPercentAdded, salt_BakersPercentAdded



######## DataFrame #########

#class recipe:
#    def __init__(self):
#        self.df = pd.DataFrame({'Ingredients': ["Levain", "AddedFlour","AddedWater","Salt"], 'Grams': [100, 500,350,10], 'BakersPercentAdded': [0.2,1,.7,.2],'BakersPercentAll':[np.nan, .931, .621, .018]})
#        self.totalDoughWeight = 960
#    def updateGrams(self,updateGrams_input):
#        self.df['Grams'] = updateGrams_input
#        self.totalDoughWeight = sum(self.df['Grams'])
#recipe = recipe()
#print(recipe.df.loc["Grams","Levain"])

######## Layout and display #########
app.layout = dbc.Container(
    [
        jumbotron,
        welcome_directions,
        table,
#        dcc.Input(id='my-id', value='initial value', type='number'),
        #html.Div(id='my-div')
    ]
)

if __name__ == "__main__":
    app.run_server(debug=False)
