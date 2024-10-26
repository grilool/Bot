import pymongo
import math
from mongo import *


async def update_curse():
    orders = order.find_one({'curseid': 1})
    #Курс с комиссией битазза
    c_bitazza = float(orders['curse_bat']) / 1.00125
    #Обновление в базе данных
    findchatid = {'curseid': 1}
    change_bitazza = {"$set": {'curse_bitazza': f"{round(c_bitazza,ndigits=3)}"}}
    order.update_one(findchatid, change_bitazza)
    #Себес курс рублей (RUB/THB)
    se_c = float(orders['curse_usdt']) / round(c_bitazza, ndigits = 3)
    se = round(se_c, ndigits = 3)
    #Обновление в базе данных
    findchatid = {'curseid': 1}
    change_rub = {"$set": {'curse_rub': f"{se}"}}
    order.update_one(findchatid, change_rub)

def nakrutka(su, val, min):
    result = order.find_one({'curseid': 1})
    if su >= min and su < 10000:
        nak = float(result['nakrutka_10'])
        return nak
    elif su >= 10000 and su <= 200000:
        nak_mi = float(result['nakrutka'])
        min = 10000
        max = 200000
        nak_ma = float(result['nakrutka_200'])
        nak = []
        nak.append(nak_mi)
        while nak_mi > nak_ma:
            nak_mi = nak_mi - float(result['shag'])
            nak_mi = round(nak_mi,ndigits = 5)
            nak.append(nak_mi)
        k = len(nak) - 1
        l = []
        d = 0
        s = 100000000000000000
        while s > k:
            if s > k:
                d += 1
                for i in range(min,max,d):
                    l.append(i)
            s = len(l)
            if len(l) > k:
                l = []
        l.append(max)
        for t in l:
            if t >= su:
                f = t
                break
        id = l.index(t)
        n = nak[id]
        return n
    elif su >= 200001 and su <= 2000000:
        nak = float(result['nakrutka_200'])
        return nak


def perevod(su, val):
    curse = order.find_one({'curseid': 1})
    sebes = round((float(curse['curse_usdt']) / float(curse['curse_bitazza'])),ndigits = 3)
    if val == 'rub':
        bat = su / round((sebes * 1.1),ndigits=3)
        bat = round(bat)
        return bat
    if val == 'usdt':
        bat = su * round((float(curse['curse_bitazza']) / 1.1),ndigits=2)
        return bat


def change_nak2(bat):
    curse = order.find_one({'curseid': 1})

    sebes = round((float(curse['curse_usdt']) / float(curse['curse_bitazza'])),ndigits = 3)

    cur_rub = sebes * 1.1
    cur_rub = round(cur_rub,ndigits=3)
    cur_usdt = float(curse['curse_bitazza']) / 1.1
    cur_usdt = round(cur_usdt,ndigits=2)


    bat = bat
    findchatid = {'id_id': 1}
    change_bat = {"$set": {'bat_min': bat}}
    const.update_one(findchatid, change_bat)

    rub = bat * cur_rub
    rub = math.ceil((rub/100))
    rub = rub * 100
    findchatid = {'id_id': 1}
    change_rub = {"$set": {'rub_min': rub}}
    const.update_one(findchatid, change_rub)

    usdt = bat / cur_usdt
    usdt = math.ceil((usdt / 10))
    usdt = usdt * 10
    findchatid = {'id_id': 1}
    change_usdt = {"$set": {'usdt_min': usdt}}
    const.update_one(findchatid, change_usdt)
    #print(sebes,cur_rub,cur_usdt,bat,rub,usdt)
