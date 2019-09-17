from pymongo import MongoClient
from foreignExchange import transform_money,call_api
from clear import get_address,get_city

import pandas as pd
import time



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

    )




    return companies_filter


def main():
    """funcion principal de mongodb"""

    db = connect()
    companies_filter = query_money_raised(db)

    data = pd.DataFrame(companies_filter)


    data["geo"] =  data.offices.apply(get_address)
    data["city"] = data.offices.apply(get_city)

    call_api()
    data["money"] = data.total_money_raised.apply(transform_money)
    # #con el filtro me quito 1000 empresas
    data_filter = data[(data.money > 0.0) & (data.geo != 0)  & (data.city != 0)]

    data_filter = data_filter[["name","city","geo","money"]]

    print(data_filter)


main()
