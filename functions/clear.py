
def get_address(col):
    """dada una o mas oficinas devuelve la latitud y longitud"""

    for office in col:
        #si tienen mas de una oficina los recorro
        if type(office[0]) == list:
            for e in office:
                print(e)
        #sino recojo directamente el valor
        else:
            print(office[0][0]["latitude"])