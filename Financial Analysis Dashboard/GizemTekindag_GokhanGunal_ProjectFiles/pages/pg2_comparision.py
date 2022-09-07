import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from mysql.connector import Error
import mysql.connector as msql
import pandas as pd
import csv
from sqlalchemy import create_engine,types
import pymysql
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/comparison_page', name='Comparison of Companies')

veritabani = msql.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="myschema"
)

yeni=veritabani.cursor()
yeni.execute("select*from myschema.mytable")

data1=[]

for i in yeni:
    data1.append(i)

all_datas = pd.DataFrame (data1, columns = ['Company_Code','Company_Name','Sector','Year','Total_Assets','Total_Liabilities','Liabilities','Shareholders_Equity','Gross_Income','Profit'])

all_datas = all_datas.reindex(columns = all_datas.columns.tolist()+["Financial_Leverage_Ratio","Debt_Equity_Ratio","Equity_Ratio","ROE","ROA"])

all_datas = all_datas.assign(Financial_Leverage_Ratio = lambda x: round(x['Total_Assets']/x['Total_Assets'] - x['Shareholders_Equity']/x['Total_Assets'],2))

all_datas = all_datas.assign(Debt_Equity_Ratio = lambda x: round(x['Total_Assets']/x['Shareholders_Equity']-x['Shareholders_Equity']/x['Shareholders_Equity'],2))

all_datas = all_datas.assign(Equity_Ratio = lambda x: round(x['Shareholders_Equity'] / x['Total_Assets'],2))

all_datas = all_datas.assign(ROE = lambda x: round(x['Profit'] / x['Shareholders_Equity'],2))

all_datas = all_datas.assign(ROA = lambda x: round(x['Profit'] / x['Total_Assets'],2))


#print(all_datas)

guncel=veritabani.cursor()
guncel.execute("SELECT * FROM myschema.mytable WHERE myschema.mytable.Year=(select max(year) from myschema.mytable)")

guncel_data=[]

for i in guncel:
    guncel_data.append(i)

datas= pd.DataFrame (guncel_data, columns = ['Company_Code','Company_Name','Sector','Year','Total_Assets','Total_Liabilities','Liabilities','Shareholders_Equity','Gross_Income','Profit'])

datas = datas.reindex(columns = all_datas.columns.tolist()+["Financial_Leverage_Ratio","Debt_Equity_Ratio","Equity_Ratio","ROE","ROA"])

datas = datas.assign(Financial_Leverage_Ratio = lambda x: round(x['Total_Assets']/x['Total_Assets'] - x['Shareholders_Equity'] / x['Total_Assets'],2))

datas = datas.assign(Debt_Equity_Ratio = lambda x: round(x['Total_Assets']/x['Shareholders_Equity']-x['Shareholders_Equity']/x['Shareholders_Equity'],2))

datas = datas.assign(Equity_Ratio = lambda x: round(x['Shareholders_Equity'] / x['Total_Assets'],2))

datas = datas.assign(ROE = lambda x: round(x['Profit'] / x['Shareholders_Equity'],2))

datas = datas.assign(ROA = lambda x: round(x['Profit'] / x['Total_Assets'],2))

cards = dbc.Row([dbc.Col(
    dbc.Card([
        html.H5('Total Assets (TL)'),
        html.H6(id='asset-card'),
        
    ],
        body=False,  
        style={'textAlign': 'center', 'color': 'dark grey'},  
        color='lightblue'  
    )
),
    dbc.Col(
        dbc.Card([
            html.H5('Shareholders Equity (TL)'),
            html.H6(id='equity-card')
        ],
            body=False,  
            style={'textAlign': 'center', 'color': 'dark grey'},  
            color='lightblue'  
        )),
    dbc.Col(
        dbc.Card([
            html.H5('Profit (TL)'),
            html.H6(id='profit-card')
        ],
            body=False,  
            style={'textAlign': 'center', 'color': 'dark grey'},  
            color='lightblue'  

        )),
        dbc.Col(
        dbc.Card([
            html.H5('Liability (TL)'),
            html.H6(id='liabilitiy-card')
        ],
            body=False,  
            style={'textAlign': 'center', 'color': 'dark grey'},  
            color='lightblue'  
        )),
        
        
        ])
    
cards2 = dbc.Row([dbc.Col(
    dbc.Card([
        html.H5('Total Assets (TL)'),
        html.H6(id='asset-card2')
     
    ],
        body=False,  
        style={'textAlign': 'center', 'color': 'dark grey'},  
        color='orange'  
    )
),
    dbc.Col(
        dbc.Card([
            html.H5('Shareholders Equity (TL)'),
            html.H6(id='equity-card2')
        ],
            body=False,  
            style={'textAlign': 'center', 'color': 'dark grey'}, 
            color='orange'  
        )),
    dbc.Col(
        dbc.Card([
            html.H5('Profit (TL)'),
            html.H6(id='profit-card2')
        ],
            body=False,  
            style={'textAlign': 'center', 'color': 'dark grey'},  
            color='orange'  

        )),
    dbc.Col(
        dbc.Card([
            html.H5('Liability (TL)'),
            html.H6(id='liabilitiy-card2')
        ],
            body=False,  
            style={'textAlign': 'center', 'color': 'dark grey'},  
            color='orange'  

        ))
        ])

layout = html.Div([dbc.Row([dbc.Col(dcc.Dropdown(id='sectordropdown1',
                                                     options=datas['Sector'].unique(),
                                                     value='Industry')),
                                dbc.Col(dcc.Dropdown(id='sectordropdown2',
                                                     options=datas['Sector'].unique(),
                                                     value='Banking'))
                                ]),

                       html.Div([
                           html.Br(),
                           dbc.Row([dbc.Col(dcc.Dropdown(id='companydropdown1')),
                                    dbc.Col(dcc.Dropdown(id='companydropdown2'))
                                    ])
                       ]),

                       html.Div([
                           html.Br(),
                           dbc.Row([
                               dbc.Col(cards),
                               dbc.Col(cards2)])
                       ]),
                       html.Div([
                           html.Br(),
                           dbc.Row([dbc.Col(dcc.RadioItems(id='data_radio1',
                                                           options={
                                                               'Total_Assets': 'Total Assets',
                                                               'Shareholders_Equity': 'Shareholders Equity',
                                                               'Profit': 'Profit',
                                                               'Liabilities' : 'Liability'
                                                           }, value='Total_Assets')),

                                    dbc.Col(dcc.RadioItems(id='data_radio2',
                                                           options={
                                                               'Total_Assets': 'Total Assets',
                                                               'Shareholders_Equity': 'Shareholders Equity',
                                                               'Profit': 'Profit',
                                                               'Liabilities' : 'Liability'
                                                           }, value='Total_Assets'))
                                    ])
                       ]),
                       html.Div([
                           html.Br(),
                           dbc.Row([dbc.Col(dcc.Graph(id='data_graph1')),
                                    dbc.Col(dcc.Graph(id='data_graph2'))
                                    ])
                       ]),

                       html.Div([
                           html.Br(),
                           dbc.Row([
                               dbc.Col([dcc.RadioItems(id='ratio_radio1',
                                                       options={
                                                           'Financial_Leverage_Ratio': 'Financial Leverage Ratio',
                                                           'Debt_Equity_Ratio': 'Debt Equity Ratio',
                                                           'Equity_Ratio': 'Equity Ratio',
                                                           'ROE': 'ROE',
                                                           'ROA': 'ROA'
                                                       }, value='Financial_Leverage_Ratio'),
                                        dcc.Graph(id='ratio_graph1')]),
                               dbc.Col([
                                   dcc.RadioItems(id='ratio_radio2',
                                                  options={
                                                      'Financial_Leverage_Ratio': 'Financial Leverage Ratio',
                                                      'Debt_Equity_Ratio': 'Debt Equity Ratio',
                                                      'Equity_Ratio': 'Equity Ratio',
                                                      'ROE': 'ROE',
                                                      'ROA': 'ROA'
                                                  }, value='Financial_Leverage_Ratio'),
                                   dcc.Graph(id='ratio_graph2')]
                               )
                           ])

                       ]),

                    html.Div([
                    html.Br(),

                    dcc.Graph(id='asset_graph',figure={})
                ]),


                    html.Div([
                    html.Br(),

                    dcc.Graph(id='share_graph_bar',figure={})
                ]),

                    html.Div([
                    html.Br(),

                    dcc.Graph(id='profit_graph_bar',figure={})
                ]),
                    html.Div([
                    html.Br(),

                    dcc.Graph(id='liability_graph_bar',figure={})
                ])
])


### ---  dropdown first column start --- ###

@callback(
    Output('companydropdown1', 'options'),
    Output('companydropdown1', 'value'),
    Input('sectordropdown1', 'value')
)
def update_companydropdown1(selected_sector):
    if selected_sector is None:
        raise PreventUpdate
    else:
        filtered_datas1 = datas[datas['Sector'] == selected_sector]
        company_options1 = filtered_datas1['Company_Name'].unique()
    return company_options1, company_options1[0]

### ---  dropdown first column end --- ###


### ---  dropdown second column start --- ###

@callback(
    Output('companydropdown2', 'options'),
    Output('companydropdown2', 'value'),
    Input('sectordropdown2', 'value')
)
def update_companydropdown2(selected_sector):
    if selected_sector is None:
        raise PreventUpdate
    else:
        filtered_datas2 = datas[datas['Sector'] == selected_sector]
        company_options2 = filtered_datas2['Company_Name'].unique()
    return company_options2, company_options2[0]

### ---  dropdown second column end --- ###

### --- cards start --- ###

@callback(
    Output('asset-card', 'children'),
    Output('equity-card', 'children'),
    Output('profit-card', 'children'),
    Output('liabilitiy-card', 'children'),
    Input('companydropdown1', 'value')
)
def update_cards(selected_company):
    filtered_datas1 = datas[datas["Company_Name"] == selected_company]
    assets = filtered_datas1["Total_Assets"]
    total_equity = filtered_datas1["Shareholders_Equity"]
    total_profit = filtered_datas1["Profit"]
    liability = filtered_datas1["Liabilities"]
    return assets, total_equity, total_profit,liability

### --- cards end --- ###

@callback(
    Output('asset-card2', 'children'),
    Output('equity-card2', 'children'),
    Output('profit-card2', 'children'),
    Output('liabilitiy-card2', 'children'),
    Input('companydropdown2', 'value')
)
def update_cards2(selected_company):
    filtered_datas1 = datas[datas["Company_Name"] == selected_company]
    assets = filtered_datas1["Total_Assets"]
    total_equity = filtered_datas1["Shareholders_Equity"]
    total_profit = filtered_datas1["Profit"]
    liability = filtered_datas1["Liabilities"]
    return assets, total_equity, total_profit, liability

### --- left top graph start --- ###

@callback(
    Output('data_graph1', 'figure'),
    Input('companydropdown1', 'value'),
    Input('data_radio1', 'value')
)
def update_data_graph(selected_company1, selected_data1):
    filtered_data1 = all_datas[all_datas['Company_Name'] == selected_company1]
    line_fig = px.line(filtered_data1,
                       x='Year',
                       y=selected_data1,
                       width=600,
                       height=350,
                       title=f'{selected_data1} for {selected_company1}')
    line_fig.update_xaxes(
        ticktext=["2017", "2018", "2019", "2020", "2021"],
        tickvals=["2017", "2018", "2019", "2020", "2021", filtered_data1.index.max()]
    )
    return line_fig

### --- left top graph end --- ###

### --- left bottom graph start --- ###

@callback(
    Output('ratio_graph1', 'figure'),
    Input('companydropdown1', 'value'),
    Input('ratio_radio1', 'value')
)
def update_ratio_graph(selected_company1, selected_data1):
    filtered_data1 = all_datas[all_datas['Company_Name'] == selected_company1]
    line_fig = px.line(filtered_data1,
                       x='Year',
                       y=selected_data1,
                       width=600,
                       height=350,
                       title=f'{selected_data1} for {selected_company1}')
    return line_fig

### --- left bottom graph end --- ###

### --- right top graph start --- ###

@callback(
    Output('data_graph2', 'figure'),
    Input('companydropdown2', 'value'),
    Input('data_radio2', 'value')
)
def update_data_graph(selected_company2, selected_data2):
    filtered_data2 = all_datas[all_datas['Company_Name'] == selected_company2]
    line_fig = px.line(filtered_data2,
                       x='Year',
                       y=selected_data2,
                       width=600,
                       height=350,
                       title=f'{selected_data2} for {selected_company2}')
    line_fig.update_xaxes(
        ticktext=["2017", "2018", "2019", "2020", "2021"],
        tickvals=["2017", "2018", "2019", "2020", "2021", filtered_data2.index.max()]
    )
    return line_fig

### --- right top graph end --- ###

### --- right bottom graph start --- ###

@callback(
    Output('ratio_graph2', 'figure'),
    Input('companydropdown2', 'value'),
    Input('ratio_radio2', 'value')
)
def update_ratio_graph(selected_company2, selected_data2):
    filtered_data2 = all_datas[all_datas['Company_Name'] == selected_company2]
    line_fig = px.line(filtered_data2,
                       x='Year',
                       y=selected_data2,
                       width=600,
                       height=350,
                       title=f'{selected_data2} for {selected_company2}')
    return line_fig

### --- right bottom graph end --- ###


### --- total assets chart start --- ###


@callback(
    Output('asset_graph','figure'),
    [Input('companydropdown1','value'),
    Input('companydropdown2','value')]
)

def update_graph_asset (selected_company1, selected_company2):
    dff = all_datas[(all_datas['Company_Name'] == selected_company1) |
             (all_datas['Company_Name'] == selected_company2)]
    barchart = px.bar(
        data_frame=dff,
        x='Year',
        y='Total_Assets',
        color='Company_Name',
        title='Total Assets Comparison',
        barmode='group'
    )
    return barchart

### --- total assets chart end --- ###

### --- shareholders equity chart start --- ###

@callback(
    Output('share_graph_bar','figure'),
    [Input('companydropdown1','value'),
    Input('companydropdown2','value')]
)

def update_graph_shareholders (selected_company1, selected_company2):
    dff = all_datas[(all_datas['Company_Name'] == selected_company1) |
             (all_datas['Company_Name'] == selected_company2)]
    bar_chart = px.bar(
        data_frame=dff,
        x='Year',
        y='Shareholders_Equity',
        color='Company_Name',
        title='Shareholders Equity Comparison',
        barmode='group'
    )
    return bar_chart

### --- shareholders equity chart end --- ###


### ---  profit histogram start --- ###

@callback(
    Output('profit_graph_bar','figure'),
    [Input('companydropdown1','value'),
    Input('companydropdown2','value')]
)

def update_graph_profit (selected_company1, selected_company2):
    dff = all_datas[(all_datas['Company_Name'] == selected_company1) |
             (all_datas['Company_Name'] == selected_company2)]
    barchart1 = px.bar(
        data_frame=dff,
        x='Year',
        y='Profit',
        color='Company_Name',
        title='Profit Comparison',
        barmode='group'
    )
    return barchart1

### ---  profit chart end --- ###

### --- liability chart start --- ###

@callback(
    Output('liability_graph_bar','figure'),
    [Input('companydropdown1','value'),
    Input('companydropdown2','value')]
)

def update_graph_liability (selected_company1, selected_company2):
    dff = all_datas[(all_datas['Company_Name'] == selected_company1) |
             (all_datas['Company_Name'] == selected_company2)]
    barchart2 = px.bar(
        data_frame=dff,
        x='Year',
        y='Liabilities',
        color='Company_Name',
        title='Liability Comparison',
        barmode='group'
    )
    return barchart2

### --- liability chart end --- ###