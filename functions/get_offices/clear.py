import pandas as pd


def get_address(col):
    """dada una o mas oficinas devuelve la latitud y longitud"""

    result = []


    #return {"type": "Point", "coordinates": [20,20]}
    dic = {}
    for office in col:
        #si tienen mas de una oficina los recorro
        """ 
        if type(office) == list:
            for e in office:
                print("yeah")
        """
        #sino recojo directamente el valor

        lat = office["latitude"]
        log = office["longitude"]
        city = office["city"]
        if lat != None and log != None:
            return {"type": "Point", "coordinates": [lat, log]}


    return 0

def get_city(col):
    """dada una o mas oficinas devuelve la latitud y longitud"""
    city = 0
    for office in col:
        city = office["city"]



    return city




