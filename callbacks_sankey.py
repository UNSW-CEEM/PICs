from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from app import app
import EnergyFlows
import figures
import pandas as pd
from dash import html
from dash import dcc
Country_List = ['Samoa','Nauru','Vanuatu','Palau','Kiribati','Cook Islands','Solomon Islands','Tonga','New Caledonia','French Polynesia','Micronesia','Niue','Tuvalu','PNG','Fiji']

@app.callback(
    [Output('Sankey_figure', 'figure'),
     Output('Sankey_elec_figure', 'figure')],
     [Input("select-year", "value"),
     Input("select-country", "value"),
]
)
def sensor_checklist(year,country):
    return figures.Generate_Sankey(year,country)[0],figures.Generate_Sankey(year,country)[1]


@app.callback(
    [Output('select-to', 'options'),
     Output('select-to', 'value')
     ],
    # Input('update-button-cross-country-to', 'n_clicks'),
    Input("select-from", "value"),

)
def update_options3(from_):
    # if n_clicks:

    items = []
    df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019, 'PNG'))
    df = df[df[' (from)'] == from_]

    #     to_list = df[' (to)'].tolist()

    for i in df[' (to)']:
        items.append(i)

    product_list = set(items)
    options = [{"label": i, "value": i} for i in product_list]
    return options,options[0]['label']




@app.callback(
    [
        # Output('cross_country_sankey_figure', 'figure'),
    Output('Hidden-Div_trend', "children"),
    Output('dynamic_callback_container', 'children')],
    [Input('update-button-cross-country-figure', 'n_clicks'),
    Input('update-button-sankey-clear-canvas', 'n_clicks')],
    [State("select-from", "value"),
    State("select-to", "value"),
     State('Hidden-Div_trend', "children"),
    State('dynamic_callback_container', 'children')
     ]
)
def update_cross_country_comparison(n_clicks,clear_canvas,from_,to_,hidden_div,div_children):
    if n_clicks != hidden_div[0]:
        values = []
        df_cross_country = pd.DataFrame()
        # to_ = to_['label']
        # print('Final ',from_,to_)

        for country in Country_List:
            df = pd.read_csv("Data/Sankey/csv/{}/{}.csv".format(2019, country))
            df = df[(df[' (from)'] == from_)&(df[' (to)']==to_)].reset_index()
            a = df[' (weight)']
            if len(a) == 0:
                a = 0
            else:
                a=a[0]
            values.append(a)

        df_cross_country['Country'] = Country_List
        df_cross_country['Values'] = values
        fig = figures.cross_country_sankey(df_cross_country,from_,to_)
        new_child = html.Div(
            style={'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
            children=[
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': n_clicks
                    },
                    figure=fig,
                ),
            ]
        )
        div_children.append(new_child)

    elif clear_canvas != hidden_div[1]:
        div_children = []

    hidden_div = [n_clicks,clear_canvas]

    return hidden_div,div_children

