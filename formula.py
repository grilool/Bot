from update import *
from mongo import *


def bat_rub(id,bat_order):
    #Поиск в дб
    adm = const.find_one({'id_id': 1})
    results = users.find_one({'chatid': id})
    curse = order.find_one({'curseid': 1})


    bat_order = bat_order
    n = nakrutka(bat_order, 'bat',float(adm['bat_min']))
    sebes = round(float(curse['curse_usdt']) / float(curse['curse_bitazza']),ndigits = 3)
    cur_rub = sebes * n
    cur_rub = round(cur_rub, ndigits = 3)
    cur_usdt = round((float(curse['curse_bitazza']) / n),ndigits = 2)

    rub = round((bat_order * cur_rub))
    usdt = round((bat_order / cur_usdt),ndigits = 2)


    bat_pro = rub / float(curse['curse_usdt']) * float(curse['curse_bitazza']) - bat_order - 20
    bat_pro = round(bat_pro)
    rub_pro = bat_pro * sebes
    rub_pro = round(rub_pro)
    usdt_pro = bat_pro / float(curse['curse_bat'])
    usdt_pro = round(usdt_pro,ndigits = 2)
    p = [bat_order,n,sebes,cur_rub,cur_usdt,rub,usdt,bat_pro,rub_pro,usdt_pro]
    return p


def rub_value(id,rub_order):
    adm = const.find_one({'id_id': 1})
    results = users.find_one({'chatid': id})
    curse = order.find_one({'curseid': 1})

    bat_order = perevod(rub_order, 'rub')
    bat_order = round(bat_order)
    n = nakrutka(bat_order, 'bat',float(adm['bat_min']))
    sebes = round((float(curse['curse_usdt']) / float(curse['curse_bitazza'])),ndigits = 3)
    c = sebes * n
    c = round(c, ndigits=3)
    bat_pro = (rub_order / sebes) - (rub_order/c) - 20
    bat_pro = round(bat_pro)
    rub_pro = bat_pro * sebes
    rub_pro = round(rub_pro)
    usdt_pro = bat_pro / float(curse['curse_bitazza'])
    usdt_pro = round(usdt_pro,ndigits = 2)
    bat = rub_order / c
    bat = round(bat)
    p = [n,sebes,c,bat_pro,rub_pro,usdt_pro,bat,bat_order]
    return p

def usdt_value(id,usdt_order):
    adm = const.find_one({'id_id': 1})
    results = users.find_one({'chatid': id})
    curse = order.find_one({'curseid': 1})

    bat_order = perevod(usdt_order, 'usdt')
    n = nakrutka(bat_order, 'udst',float(adm['bat_min']))
    c = round(float(curse['curse_bitazza']) / n,ndigits=2)
    bat = usdt_order * c
    bat = round(bat)

    sebes = round(float(curse['curse_bitazza']), ndigits=2)
    bat_pro = sebes * usdt_order - bat - 20
    bat_pro = round(bat_pro)
    rub_pro = bat_pro * round((float(curse['curse_usdt']) / float(curse['curse_bitazza'])),ndigits=3)
    rub_pro = round(rub_pro)
    usdt_pro = bat_pro / sebes
    usdt_pro = round(usdt_pro,ndigits=2)
    p = [n,c,sebes,bat,bat_pro,rub_pro,usdt_pro,bat_order]
    return p
