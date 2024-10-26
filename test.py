nak_mi = 1.03
min = 10000
max = 200000
nak_ma = 1.01
nak = []
nak.append(nak_mi)
while nak_mi > nak_ma:
    nak_mi = nak_mi - 0.0001
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
su = 50000
for t in l:
    if t >= su:
        f = t
        break
id = l.index(t)
print(nak)
print(l)
print(l[id],nak[id])


result = users.find_one({'chatid': message.chat.id})
if result == None:
    useradd = {
        'username': message.from_user.username,
        'chatid': message.chat.id,
        'FirstName': message.from_user.first_name,
        'LastName': message.from_user.last_name,
        'adm': 0,
        'price': 0,
        'banned': False,
        'rub_order': 0,
        'bat_order':0,
        'usdt_order': 0,
        'ref': 0,
        'latitude': 0,
        'longitude': 0,
        }
    results = users.insert_one(useradd)
    print(f"Add database id: {results.inserted_id}")
    text = text_menu
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Расчитать', callback_data = 'search')
    builder.button(text = 'Способы получения', callback_data = 'delivery')
    builder.button(text = 'Общая информация', callback_data = 'info')
    builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
    builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
    builder.adjust(1,1,1,1,1)
    await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(one_time_keyboard=True,resize_keyboard=True), parse_mode="HTML")
elif result != None:
    text = text_menu
    if result['banned'] == True:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        await message.bot.send_message(chat_id = message.chat.id, text = 'К сожалению Ваш аккаунт заблокирован', reply_markup = builder.as_markup())
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Расчитать', callback_data = 'search')
        builder.button(text = 'Способы получения', callback_data = 'delivery')
        builder.button(text = 'Общая информация', callback_data = 'info')
        builder.button(text = 'Написать оператору', url = 'https://t.me/Misha_Thai_Baht')
        builder.button(text = 'Отзывы', url = 'https://t.me/misha_obmen_thb')
        builder.adjust(1,1,1,1,1)
        await message.bot.send_message(chat_id = message.chat.id, text = text, reply_markup = builder.as_markup(one_time_keyboard=True,resize_keyboard=True), parse_mode="HTML")
