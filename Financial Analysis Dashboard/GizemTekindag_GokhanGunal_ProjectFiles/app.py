import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import dash_auth
from mysql.connector import Error
import mysql.connector as msql
from sqlalchemy import create_engine, types
import pymysql
import pandas as pd

#Connection the database and creation of schema-------------------------------------------------------------------------------------

try:
    conn = msql.connect(
        host="localhost",
        user="root",
        password="12345678")
    if conn.is_connected():
        cursor=conn.cursor()
        cursor.execute("CREATE DATABASE myschema")
        print("database created")
except Error as e:
    print("Error while connecting to MySQL", e)


#Saving the table and schema-------------------------------------------------------------------------------------------------------------------

engine=create_engine('mysql+pymysql://root:12345678@localhost/myschema')
df=pd.read_csv("financials.csv") # Reading the csv, (for mac, sep=',') 
df.to_sql('mytable',con=engine,index=False, if_exists='replace') # Saving csv to the mytable 

veritabani=msql.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="userschema"
)

yeni=veritabani.cursor()
yeni.execute("select*from userschema.usertable")

users=[]

for i in yeni:
    users.append(i)

usersDict={}

for d in range(len(users)):
    usersDict[users[d][1]]=users[d][2]


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server=app.server

auth=dash_auth.BasicAuth(
    app,usersDict
)
#We create usertable in MYSQL, user information comes from database.

navbar = dbc.NavbarSimple(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"), 
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
    brand="Financial Analysis Dashboard",
    fluid=True,
    brand_href="#",
    color="primary",
    dark=True,
)

app.layout = html.Div([
            dbc.Row(
                [
                    dbc.NavbarSimple(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
    brand="Financial Analysis Dashboard",
    fluid=True,
    brand_href="#",
    color="primary",
    dark=True,
)
                    
                ]),
                html.Br(),

            dbc.Row(
                [
                    html.Br(),
                    dash.page_container
                ]) 
])

if __name__ == "__main__":
    app.run_server(debug=False)