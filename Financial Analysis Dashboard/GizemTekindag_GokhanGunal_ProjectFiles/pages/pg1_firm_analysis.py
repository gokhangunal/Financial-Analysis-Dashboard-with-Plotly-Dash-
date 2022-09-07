import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from mysql.connector import Error
import mysql.connector as msql
import pandas as pd
import csv
from sqlalchemy import create_engine, types
import pymysql
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate

veritabani=msql.connect(
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


dash.register_page(__name__, path='/', # '/' is home page
                                name='Firm Analysis',
                                         description='Financial Analysis Dashboard with bar charts, histograms and pie charts')

leverageRatio_card = dbc.Card([
    html.H5('Financial Leverage Ratio'),
    html.H6(id='leverageRatio_card')
], body=False,
    style={'textAlign': 'center', 'color': 'dark grey'},
    color='lightblue',
    className="w-50 mb-3"
)

debtEquityRatio_card = dbc.Card([
    html.H5('Debt Equity Ratio'),
    html.H6(id='debtEquityRatio_card')
], body=False,
    style={'textAlign': 'center', 'color': 'dark grey'},
    color='lightblue',
    className="w-50 mb-3"
)

equityRatio_card=dbc.Card([
    html.H5('Equity Ratio'),
    html.H6(id='equityRatio_card')
], body=False,
    style={'textAlign': 'center', 'color': 'dark grey'},
    color='lightblue',
    className="w-50 mb-3"
)
ROE_card=dbc.Card([
    html.H5('Return On Equity'),
    html.H6(id='roe_card')
], body=False,
    style={'textAlign': 'center', 'color': 'dark grey'},
    color='lightblue',
    className="w-50 mb-3"
)
ROA_card=dbc.Card([
    html.H5('Return on Assets'),
    html.H6(id='roa_card')
], body=False,
    style={'textAlign': 'center', 'color': 'dark grey'},
    color='lightblue',
    className="w-50 mb-3"
)

cards=html.Div([leverageRatio_card,debtEquityRatio_card,equityRatio_card,ROE_card,ROA_card
    
])

layout=html.Div([
    dbc.Row([
        dbc.Col(dcc.Dropdown(id="sector_dropdown", options=datas['Sector'].unique(),value='Industry')),
        dbc.Col(dcc.Dropdown(id="company_dropdown",options=[],value='')),
        dbc.Col(dcc.Dropdown(id="year_dropdown", options=[],value='')),
    ]),

    dbc.Row([
    
        
    dbc.Col(children=[html.Br(),html.Br(),html.Br(),html.Div(cards)]),
    dbc.Col(children=[html.Div(dcc.Graph(id='assest_graph', figure={}))]),
    
    ]),
    dbc.Row([dbc.Col(dcc.Graph(id='equity_graph', figure={})),
            dbc.Col(dcc.Graph(id='profit_graph', figure={}))
    
    ]),

        dbc.Row([dbc.Col(dcc.Graph(id='liabilities_graph', figure={})),
            dbc.Col(dcc.Graph(id='total_liabilities_graph', figure={}))
    
    ])

])

@callback(
    Output('company_dropdown', 'options'),
    Output('company_dropdown', 'value'),
    Input('sector_dropdown', 'value')
)
def update_company_dropdown(selected_sector):
    if selected_sector is None:
        raise PreventUpdate
    else:
        filtered_data=datas[datas['Sector']==selected_sector]
        company_options=filtered_data['Company_Name'].unique()
        return company_options,company_options[0]

@callback(
    Output('year_dropdown','options'),
    Output('year_dropdown','value'),
    Input('company_dropdown', 'value')
)
def update_year(selected_company):
    if selected_company is None:
        raise PreventUpdate
    else:
        filtered_data=all_datas[all_datas['Company_Name']==selected_company]
        year_value=filtered_data['Year'].unique()
    return year_value, year_value[0]

@callback(
    Output('leverageRatio_card','children'),
    Output('debtEquityRatio_card','children'),
    Output('equityRatio_card','children'),
    Output('roe_card','children'),
    Output('roa_card','children'),
    Input('sector_dropdown', 'value'),
    Input('company_dropdown', 'value'),
    Input('year_dropdown', 'value')
)
def update_cards(selected_sector,selected_company,selected_year):
    filtered_data=all_datas[(all_datas['Sector']==selected_sector)&(all_datas['Company_Name']==selected_company)&(all_datas['Year']==selected_year)]
    leverageRatio=filtered_data['Financial_Leverage_Ratio']
    debtEquityRatio=filtered_data['Debt_Equity_Ratio']
    equityRatio=filtered_data['Equity_Ratio']
    roe=filtered_data['ROE']
    roa=filtered_data['ROA']
    return leverageRatio,debtEquityRatio,equityRatio,roe,roa

@callback(
    Output('assest_graph','figure'),
    Output('equity_graph','figure'),
    Output('profit_graph','figure'),
    Output('liabilities_graph','figure'),
    Output('total_liabilities_graph','figure'),
    Input('sector_dropdown', 'value'),
    Input('company_dropdown', 'value')
)
def update_graphs(selected_sector,selected_company):
    filtered_data=all_datas[(all_datas['Sector'] == selected_sector) & (all_datas['Company_Name'] == selected_company)]
    asset = px.bar(
                    data_frame=filtered_data,
                    x='Year',
                    y='Total_Assets',
                    width=800,
                    height=500,
                    title=f'Total Assets of {selected_company} in years')
    equity = px.bar(
                    data_frame=filtered_data,
                    x='Year',
                    y='Shareholders_Equity',
                    width=800,
                    height=500,
                    title=f'Total Shareholders Equity of {selected_company} in years')
    profit = px.bar(
                    data_frame=filtered_data,
                    x='Year',
                    y='Profit',
                    width=800,
                    height=500,
                    title=f'Total Profit of {selected_company} in years'
    )
    liability = px.bar(
                    data_frame=filtered_data,
                    x='Year',
                    y='Liabilities',
                    width=800,
                    height=500,
                    title=f'The indebtedness of {selected_company} in years'
    )

    total_liabilitiy =px.bar(
                    data_frame=filtered_data,
                    x='Year',
                    y='Total_Liabilities',
                    width=800,
                    height=500,
                    title=f'Total Liabilities of {selected_company} in years'
    )
    return asset,equity,profit,liability,total_liabilitiy