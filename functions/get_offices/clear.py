import numpy as np

def get_address(col):
    """dada una o mas oficinas devuelve la latitud y longitud"""
    lat = col[0]
    log = col[1]

    if not np.isnan(lat) and not np.isnan(log):
        return {"type": "Point", "coordinates": [log, lat]}


    return 0






