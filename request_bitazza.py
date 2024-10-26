import requests
from fake_useragent import UserAgent
from datetime import datetime as dt
import asyncio
import pymongo
from mongo import *


#client = pymongo.MongoClient('localhost',username='AdminMongo', password='Grilool1234',authMechanism='SCRAM-SHA-1')


async def usdt_thb_update():
    d = dt.now()
    day = d.strftime("%d")
    year = d.strftime("%Y")
    month = d.strftime("%m")
    hour = d.strftime("%H")
    minute = d.strftime("%M")
    url = f"https://apexapi.bitazza.com:8443/AP/GetTickerHistory?InstrumentId=5&OMSId=1&Interval=900&FromDate={year}-{month}-{day}T{hour}%3A{minute}%3A00Z&ToDate={year}-{month}-{day}T{hour}%3A{minute}%3A00Z"
    ua = UserAgent(browsers=['chrome'],os='windows',platforms='pc')
    userAgent = ua.random
    headers = {"UserAgent": userAgent}
    response = requests.get(url = url, headers = headers)
    r = response.json()
    r = r[0]
    Get_curse_usdt = f"{r[1]}"

    findchatid = {'curseid': 1}
    change_bat = {"$set": {'curse_bat': Get_curse_usdt}}
    order.update_one(findchatid, change_bat)
