import requests
from fake_useragent import UserAgent
import asyncio
from datetime import datetime as dt
import pymongo



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
print(r[0][7])
