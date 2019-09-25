import pandas as pd
from pandas.io.json import json_normalize


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

def average(col):
    avg = 0
    for k,v in col.items():
        avg += v

    return avg/len(col)

def getCoord():

    data = getOffice()
    filters = ["starbucks", "nursery", "club", "vegan"]


    for filter in filters:
        data["point"] = data[["point", "latitude", "longitude"]].apply(count_locals, args=(filter,), axis=1)
        

    data.to_json("path.json",orient="records")

    data = pd.read_json("path.json")
    data["point"] = data.point.apply(average)
    result = data.sort_values(['point'], ascending=[0])
    result = result.drop_duplicates(subset='city', keep="first")

    #obtengo el mejor
    max_df = result.iloc[:1].copy()

    max_df["filters"] = max_df[["latitude", "longitude"]].apply(getLocals, args=(filters,), axis=1)

    #data = json_normalize(json.loads(df_json), 'offices', ['name', 'total_money_raised', 'category_code'])
    a = max_df.explode("filters")
    a = json_normalize(a["filters"])


    result = max_df.append(a, ignore_index=True)

    # por último obtengo las oficinas cercanas
    db = connect()
    max_point = result.loc[0,].copy()
    offices = geonear(max_point.geo, 2000, db)

    lst = []
    for office in offices:
        lst.append(office)

    a = json_normalize(lst)
    a = a[["name","city","money","category_code","longitude","latitude"]]

    result = result.append(a, ignore_index=True)

    #limpio las columnas
    result = result[["name", "city", "money", "category_code", "longitude", "latitude","point"]]

    result.update(result[["point"]].fillna(0))
    result.update(result[["city"]].fillna(max_point.city))
    result.to_json("result.json", orient="records")
    return result




#lo pongo aqui por problemas de depedencias ciruclares
from mongo import getOffice, geonear,connect
from foursquare import count_locals,getLocals
