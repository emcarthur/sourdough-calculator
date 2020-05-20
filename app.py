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

df = pd.DataFrame({'Ingredients': ["Levain", "AddedFlour","AddedWater","Salt"], 'Grams': [100.123, 500,350,10], 'BakersPercentAdded': [0.2123,1,.7,.2],'BakersPercentAll':[np.nan, .931, .621, .018]})
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
            [ #str(np.round(df.loc["Levain","Grams"]))
                dbc.Input(id='my-id',value=2, type="number", step=.1,min=0,style={'backgroundColor': '#c1e6bd'}),
                dbc.InputGroupAddon("g", addon_type="append"),
            ]
        )
levain_percent = dbc.InputGroup(
            [ #value=100*np.round(df.loc["Levain","BakersPercentAdded"],3),
                dbc.Input(id='my-div',value = 4, type="number", step=.1,min=0,max=100,style={'backgroundColor': '#cddaf6'}),
                dbc.InputGroupAddon("%", addon_type="append"),
            ]
        )

######### Table #########

table_header = [
    html.Thead(html.Tr([html.Th("Ingredients"), html.Th("Amount(g)"),html.Th("Bakers Percentage of ADDED flour"), html.Th("Bakers Percentage of ALL flour"), html.Th("True Percentage by weight")]))
]

levain_row = html.Tr([html.Td(levain_tooltip),html.Td(levain_grams), html.Td(levain_percent), html.Td("20 %"),  html.Td("10.4 %")])
flour_row = html.Tr([html.Td("Added Flour"),html.Td(2), html.Td("1"), html.Td("20 %"),  html.Td("10.4 %")])
water_row = html.Tr([html.Td("Added Water"),html.Td("1"), html.Td("1"), html.Td("20 %"),  html.Td("10.4 %")])
salt_row = html.Tr([html.Td("Salt"),html.Td("1"), html.Td("1"), html.Td("20 %"),  html.Td("10.4 %")])
total_row = html.Tr([html.Td("Total dough weight", style={'borderTopWidth': '3px'}), html.Td("500", style={'borderTopWidth': '3px'})])
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
            ] ,style={"margin-top": "-20px"})

    ]
)

######## call backs ############3

@app.callback(
    Output(component_id='my-div', component_property='value'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return np.round(100*(input_value/df.loc["AddedFlour","Grams"]),1)

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
    app.run_server(debug=True)
