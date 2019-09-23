from pymongo import MongoClient
from foreignExchange import transform_money,call_api
from clear import get_address
from pandas.io.json import json_normalize

import pandas as pd
import time
import json
import os


def connect():
    """funcion que conecta a la base de datos"""
    client = MongoClient("mongodb://localhost:27017/")
    db = client.companies 

    return db

def query_money_raised(db):
    """filtra las compañia que han ganado mas de 0 dorales y tiene minimo 10 años"""

    #consigo el año actual y le resto 10
    try:
        year = int(time.strftime("%Y")) - 10
    except:
        raise("Error a conventir la fecha")

    
    companies_filter = db.companies.find(
        {
            "total_money_raised":{"$ne":"$0"},
            "founded_year": {"$gte":year},
        },
        {
            "_id":0
        }
    )




    return companies_filter

def prueba(col):
    #print(col)
    a = 0
    if col != []:
        pass
        #print(json_normalize(col[0],max_level=100))
        #return json_normalize(col[0],max_level=100)


def get_json():
    """funcion principal de mongodb"""

    db = connect()
    companies_filter = query_money_raised(db)
    data = pd.DataFrame(companies_filter)

    #print(data.offices[10])
    #print(json_normalize(data.offices[10]))
    #dataframe de la columna officee
    #df1 = (pd.concat({i: json_normalize(x) for i, x in data.pop('offices').items()}))
    #print(df1)

    #consigo las oficinas por empresas
    df_json = data.to_json(orient='records')
    #aplano oficionas, y me quedo con nombre, capital y la categoria de la empresa
    data = json_normalize(json.loads(df_json),'offices',['name', 'total_money_raised','category_code'])

    data["geo"] =  data[["latitude","longitude"]].apply(get_address,axis = 1)

    #llamo a la api de cambio de divisas
    call_api()
    data["money"] = data.total_money_raised.apply(transform_money)
    data_filter = data[(data.money > 0.0) & (data.geo != 0)  & (data.city != 0)]

    data_filter = data_filter[["name","city","geo","money","category_code","longitude","latitude",]]

    path = os.path.join(os.path.dirname(__file__), '../../json/db.json')

    data_filter.to_json(path,orient="records")


