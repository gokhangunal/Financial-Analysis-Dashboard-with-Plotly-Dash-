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

dash.register_page(__name__, path='/sector_analysis', name='Sector Analysis')

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

layout =html.Div([
                    dbc.Row([dbc.Col(dcc.Dropdown(id='first_sector_dd',
                                options=datas['Sector'].unique(),
                                    value='Industry')),
                            dbc.Col(dcc.Dropdown(id='second_sector_dd',
                                options=datas['Sector'].unique(),
                                    value='Industry'))
                            ]),

                html.Div([
                html.Br(),
                    dbc.Row([dbc.Col(dcc.Dropdown(id='first_year_dd')),
                            dbc.Col(dcc.Dropdown(id='second_year_dd'))
                           ])]),
                    
                html.Div([
                           html.Br(),
                           dbc.Row([dbc.Col(dcc.Graph(id='first_pie')),
                                    dbc.Col(dcc.Graph(id='first_bar'))
                                    ])
                       ]),
                html.Div([
                           html.Br(),
                           dbc.Row([dbc.Col(dcc.Graph(id='second_pie')),
                                    dbc.Col(dcc.Graph(id='second_bar'))
                                    ])
                       ]),
                html.Div([
                           html.Br(),
                           dbc.Row([dbc.Col(dcc.Graph(id='third_pie')),
                                    dbc.Col(dcc.Graph(id='third_bar'))
                                    ])
                       ]),
                html.Div([
                           html.Br(),
                           dbc.Row([dbc.Col(dcc.Graph(id='fourth_pie')),
                                    dbc.Col(dcc.Graph(id='fourth_bar'))
                                    ])
                       ])
])

### ---  dropdown third column start --- ###

@callback(
    Output('first_year_dd', 'options'),
    Output('first_year_dd', 'value'),
    Input('first_sector_dd', 'value')
)
def update_sectordropdown3(selected_sector):
    if selected_sector is None:
        raise PreventUpdate
    else:
        filtered_datas1 = all_datas[all_datas['Sector'] == selected_sector]
        sector_options1 = filtered_datas1['Year'].unique()
    return sector_options1, sector_options1[0]

### ---  dropdown third column end --- ###

### ---  dropdown fourth column start --- ###

@callback(
    Output('second_year_dd', 'options'),
    Output('second_year_dd', 'value'),
    Input('second_sector_dd', 'value')
)
def update_sectordropdown4(selected_sector):
    if selected_sector is None:
        raise PreventUpdate
    else:
        filtered_datas2 = all_datas[all_datas['Sector'] == selected_sector]
        sector_options2 = filtered_datas2['Year'].unique()
    return sector_options2, sector_options2[0]

### ---  dropdown fourth column end --- ###



### --- chained sector pie chart start pg3---###

@callback(
    Output('first_pie','figure'),
    Input('first_year_dd','value'),
    Input('first_sector_dd', 'value')
)

def pie_graph_for_asset (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector)& (all_datas['Year'] == selected_year)]
    piechart1 = px.pie(
        data_frame=df,
        values='Total_Assets',
        names='Company_Name',
        color='Company_Name',
        hole=0.5,
        width=800,
        height=500,
        title='Companies'+"'"+ ' Total Assets on Sectoral Basis',
    )
    return piechart1

### --- chained sector pie chart end pg3---###

### --- chained sector bar chart start pg3---###

@callback(
    Output('first_bar','figure'),
    Input('second_year_dd','value'),
    Input('second_sector_dd', 'value')
)

def bar_graph_for_asset (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector) & (all_datas['Year'] == selected_year)]
    barchart1 = px.bar(
        data_frame=df,
        x='Total_Assets', y='Company_Name',
        title='Sector Comparison According to Total Asset',
        width=800,
        height=500,
        color='Company_Name'
    )
    return barchart1

##########################################

@callback(
    Output('second_bar','figure'),
    Input('second_year_dd','value'),
    Input('second_sector_dd', 'value')
)

def bar_graph_for_shareholders_equity (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector) & (all_datas['Year'] == selected_year)]
    barchart2 = px.bar(
        data_frame=df,
        x='Shareholders_Equity', y='Company_Name',
        title='Sector Comparison According to Total Shareholders Equity',
        width=800,
        height=500,
        color='Company_Name'
    )
    return barchart2


@callback(
    Output('second_pie','figure'),
    Input('first_year_dd','value'),
    Input('first_sector_dd', 'value')
)

def pie_graph_for_shareholders_equity (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector)& (all_datas['Year'] == selected_year)]
    piechart2 = px.pie(
        data_frame=df,
        values='Shareholders_Equity',
        names='Company_Name',
        color='Company_Name',
        hole=0.5,
        width=800,
        height=500,
        title='Companies'+"'"+ ' Total Shareholders Equity on Sectoral Basis',
    )
    return piechart2

##########################################

@callback(
    Output('third_bar','figure'),
    Input('second_year_dd','value'),
    Input('second_sector_dd', 'value')
)

def bar_graph_for_profit (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector) & (all_datas['Year'] == selected_year)]
    barchart3 = px.bar(
        data_frame=df,
        x='Profit', y='Company_Name',
        title='Sector Comparison According to Total Profit',
        width=800,
        height=500,
        color='Company_Name'
    )
    return barchart3


@callback(
    Output('third_pie','figure'),
    Input('first_year_dd','value'),
    Input('first_sector_dd', 'value')
)

def pie_graph_for_profit (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector)& (all_datas['Year'] == selected_year)]
    piechart3 = px.pie(
        data_frame=df,
        values='Profit',
        names='Company_Name',
        color='Company_Name',
        hole=0.5,
        width=800,
        height=500,
        title='Companies'+"'"+ ' Total Profit on Sectoral Basis',
    )
    return piechart3

#############################

@callback(
    Output('fourth_bar','figure'),
    Input('second_year_dd','value'),
    Input('second_sector_dd', 'value')
)

def bar_graph_for_liability (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector) & (all_datas['Year'] == selected_year)]
    barchart3 = px.bar(
        data_frame=df,
        x='Liabilities', y='Company_Name',
        title='Sector Comparison According to Liability',
        width=800,
        height=500,
        color='Company_Name'
    )
    return barchart3


@callback(
    Output('fourth_pie','figure'),
    Input('first_year_dd','value'),
    Input('first_sector_dd', 'value')
)

def pie_graph_for_liability (selected_year,selected_sector):
    df = all_datas[(all_datas['Sector'] == selected_sector)& (all_datas['Year'] == selected_year)]
    piechart3 = px.pie(
        data_frame=df,
        values='Liabilities',
        names='Company_Name',
        color='Company_Name',
        hole=0.5,
        width=800,
        height=500,
        title='Companies'+"'"+ ' Liability on Sectoral Basis',
    )
    return piechart3