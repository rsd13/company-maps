from pymongo import MongoClient
from foreignExchange import transform_money,call_api
from clear import get_address

import pandas as pd
import time

print(time.strftime("%Y"))

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

    
    companies_filter = db.companies.find({
        "total_money_raised":{"$ne":"$0"},
        "founded_year": {"$gte":2009}
        }
    )

    return companies_filter


def main():
    """funcion principal de mongodb"""

    db = connect()
    companies_filter = query_money_raised(db)

    data = pd.DataFrame(companies_filter)
    print(data)


    #data.offices.apply(get_address)
 
    #call_api()
    #data["prueba"] = data.total_money_raised.apply(transform_money)
    #con el filtro me quito 1000 empresas
    #data_filter = data[(data.prueba > 0.0)] 
    

main()