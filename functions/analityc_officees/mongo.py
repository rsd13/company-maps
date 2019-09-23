
from pymongo import MongoClient
import pandas as pd
from analityc import init_geo

def connect():
    """funcion que conecta a la base de datos"""
    client = MongoClient("mongodb://localhost:27017/")
    db = client.companies

    return db


def getCollection(db):
    """funcion que devuelve resultados tras una query"""
    return db.location.find(
        {},{"_id":0}
    )

def geonear(geopoint, maxdistance, db):
    """funcion quee aplica el filtro near de monbofb"""
    return db.location.find({
        "geo":{
            "$near":{
                "$geometry":geopoint,
                "$maxDistance":maxdistance
            }
        }
    })


def getOffice():


    db = connect()
    companies = getCollection(db)
    data = pd.DataFrame(companies)
    data["point"] = data.geo.apply(init_geo, args=(db,))

    return data


#lo pongo debajo por problemas de dependencias circulares
