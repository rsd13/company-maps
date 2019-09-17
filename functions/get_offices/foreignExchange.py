
import re
import os
import requests
import json

from os.path import join, dirname
from dotenv import load_dotenv


MONEY = {
    "k":1000,
    "K":1000,
    "M":1000000,
    "m":1000000,
    "B":1000000000,
    "b":1000000000,
}

SYMBOLS = {
    "$": "USD",
    "€": "EUR",
    "£": "GBP",
    "¥": "JPY",
    "C$": "CAD",
    "kr": "DKK"
}

COINS = {
    "USD":0,
    "EUR":1,
    "GBP":0,
    "JPY":0,
    "CAD":0,
    "DKK":0,
}

#lo pongo fuera para que se carge solo 1 vez 


def call_api():
    """metodo que llama a la api y obtiene el cambio de divisas en un diccionario """
    #obtengo la keet secreta
    
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    SECRET_KEY = os.environ.get("MONEY_KEY")

    coins = ["USD","GBP","JPY","CAD","DKK"]
    for coin in coins:
        url = "https://api.cambio.today/v1/full/{}/json?key={}".format(coin,SECRET_KEY)
        re = requests.get(url)
        re_json =  json.loads(re.text) 
        lst = re_json["result"]["conversion"]

        for e in lst:
            if e["to"] == "EUR":
                COINS[coin] = e["rate"]
   
    

def transform_money(col):
    
    #transformo la lista de regex en un string
    nums = ''.join(re.findall("[\d]", col))
    #me quedo con la cantidad k,M...
    count_money = col[-1]
    #me quedo con el tipo de moneda
    symbols = col[0]
    if symbols == "C":
        #para obtener C$
        symbols += col[1]
    elif symbols == "k":
        #para obtener kr
        symbols += col[1]
    
   
    symbol = SYMBOLS.get(symbols)
    #solo llamo cuando no seas dorales


    try:
        count_money = MONEY.get(count_money)
        count = COINS.get(symbol)
        num = int(nums) * count * count_money
       
    except:
        num = 0
   
    #si es mayot que 1M
   
    if num >= 1000000:
        return num
    else:
        return 0



