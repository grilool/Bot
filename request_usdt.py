import requests
from fake_useragent import UserAgent
import asyncio
import pymongo
from mongo import *
#client = pymongo.MongoClient('localhost',username='AdminMongo', password='Grilool1234',authMechanism='SCRAM-SHA-1')


async def usdt_rub_update():
    params = {"userId": "", "tokenId": "USDT", "currencyId": "RUB", "payment": ["382"], "side": "1", "size": "10", "page": "1", "amount": 49500}
    ua = UserAgent(browsers=['chrome'],os='windows',platforms='pc')
    userAgent = ua.random
    headers = {"UserAgent": userAgent}
    response = requests.post(url = "https://api2.bybit.com/fiat/otc/item/online", data = params, headers = headers)
    d = response.json()
    r = d['result']
    k = r['items']

    f1 = k[0]
    price_1 = float(f1['price'])

    f2 = k[1]
    price_2 = float(f2['price'])

    f3 = k[2]
    price_3 = float(f3['price'])

    f4 = k[3]
    price_4 = float(f4['price'])

    f5 = k[4]
    price_5 = float(f5['price'])

    g = [float(price_1),float(price_2),float(price_3),float(price_4),float(price_5)]
    sr = f"{round((sum(g) / len(g)),ndigits = 2)}"


    findchatid = {'curseid': 1}
    change_usdt = {"$set": {'curse_usdt': sr}}
    order.update_one(findchatid, change_usdt)
