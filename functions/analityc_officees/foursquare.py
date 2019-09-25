import os
import requests
import json

from os.path import join, dirname
from dotenv import load_dotenv
from analityc import count

#parte de codigo para reecoger las keys
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

#url general para llamar a la api
url = 'https://api.foursquare.com/v2/venues/explore'

def get_query(lat,long,query = '', radius = 1000, cod = ''):
    coord = str(lat) + "," + str(long)
    params = dict(
        client_id=client_id,
        client_secret=client_secret,
        v='20180323',
        ll=coord,
        query=query,
        radius=radius,
        categoryId=cod,
        # limit=5
    )
    return params


def call_api(lat,long, filter):
    if filter == "starbucks":
        params = get_query(lat, long, query="starbucks")
    else:
        params = get_query(lat, long, cod=codes[filter])

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    return data

codes = {
    "vegan":"4bf58dd8d48988d1d3941735",
    "nursery": "4f4532974b9074f6e4fb0104",
    "club":"4bf58dd8d48988d11f941735",
    "aeroport": "4bf58dd8d48988d1ed931735",
}



def count_locals(col, filter):
    """
    :param col: [points,lat,long]
    :param filter: filtro para buscar un tipo de local en la api
    :return: devuelve el diccionario points actualizado
    """

    point = col[0]
    lat = col[1]
    long = col[2]

    data = call_api(lat, long, filter)

    #consigo el total de locales de la busqueda
    count_filter = len(data["response"]["groups"][0]["items"])
    #actualizo las puntuaciones
    point[filter] = count(count_filter)

    return point


def getLocals(col,filters):


    lat = col[0]
    long = col[1]


    result = []
    for filter in filters:
        data = call_api(lat,long,filter)

        for item in data["response"]["groups"][0]["items"]:
            dic = {}
            dic["name"] = item["venue"]["name"]
            dic["longitude"] = item["venue"]["location"]["lat"]
            dic["latitude"] = item["venue"]["location"]["lng"]
            dic["category_code"] = item["venue"]["categories"][0]["name"]
            result.append(dic)
    return result
