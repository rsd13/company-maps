

cats = ["mobile", "web", "software", "ecommerce", "analytics", "games_video", "web", "network_hosting", "games_video"]

def count_cat(companies):
    """cuenta las companias con las categorias de tecnologias """
    count = 0
    for com in companies:
        if com["category_code"] in cats:
            count += 1

    return count


def init_geo(geo, db, tam=2000):

    companies = geonear(geo, tam, db)
    count_companies = companies.count()
    dic = {
        "companies_money": 0,
        "technology_companies": 0,
        "old_companies": 0,
        "nursery": 0,
        "vegan": 0,
        "aeroport": 0,
        "club": 0,
        "starbucks": 0
    }

    if count_companies > 0:
        count_cats = count_cat(companies)
        #cuento las empresas tecnologicas


        if count_cats > 0:
            dic["technology_companies"] = count(count_cats)

        #cuento las empresas con mas de 1M y las antiguas al mismo tiempo
        #por el filtro hecho en mongodb
        dic["companies_money"] = count(count_companies)
        dic["old_companies"] = count(count_companies)
    return dic


def count(num):
    """
    funcion que cuenta hasta con el siguiente filtro:

    . Si encuentra 1 le suma 0.2, a los siguiebtes se le va sumando 0.1 hasta un limite de 1
    :return:
    """

    result = 0
    if num == 1:
        result =  0.2
    else:
        aux = num - (num - 1)

        result = (aux*0.2) + ((num-1)*0.1)

    if result >=1:
        result =  1

    return result


def getDataframe():

    data = getOffice()

    """data["point"] = data[["point", "latitude", "longitude"]].apply(count_locals, args=("starbucks",), axis=1)
    data["point"] = data[["point", "latitude", "longitude"]].apply(count_locals, args=("nursery",), axis=1)
    data["point"] = data[["point", "latitude", "longitude"]].apply(count_locals, args=("club",), axis=1)
    data["point"] = data[["point", "latitude", "longitude"]].apply(count_locals, args=("vegan",), axis=1)

    data.to_json("path.json",orient="records")"""

#lo pongo aqui por problemas de depedencias ciruclares
from mongo import getOffice, geonear
from foursquare import count_locals
