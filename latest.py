#Размещение заказа бат - руб
@dp.callback_query(lambda c: c.data.startswith('create_order_bat_rub'))
async def rub(call: types.CallbackQuery,state: FSMContext):
        d = dt.utcnow()
        f = timedelta(hours = 3)
        d = d + f
        id = call.data.replace('create_order_bat_rub!', '')
        id = int(id)
        for t in temp.find({'chatid': call.message.chat.id}):
            if t['id'] == id and t['fiat'] == 'bat' and order_wh == 'USDT':
                temp.delete_one({'id': id, 'fiat':'bat'})
                await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
                temptime = t['time']
                ordertime = d - temptime
                ordertime = round(ordertime.total_seconds())
                if ordertime > 1800:
                    text = 'Время размещения заказа вышло, пожалуйста сделайте новый расчет.'
                    builder = InlineKeyboardBuilder().button(text = 'Главное меню', callback_data = 'menu')
                    await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
                if ordertime < 1800:
                    #orderid
                    ord = []
                    day = d.strftime("%d")
                    year = d.strftime("%Y")
                    month = d.strftime("%m")
                    date = f"{day}{month}{year}"
                    for orders in order.find({ 'date': date}):
                        ord.append(orders)
                    orderid = date + f"{len(ord) + 1}"
                    #поиск
                    adm = const.find_one({'id_id': 1})
                    results = users.find_one({'chatid': call.message.chat.id})
                    curse = order.find_one({'curseid': 1})
                    #Курс
                    bat_order = t['bat']
                    n = t['n']
                    sebes = t['sebes']
                    cur_rub = t['curse_rub']
                    cur_usdt = t['curse_usdt']
                    rub = t['rub']
                    usdt = t['usdt']

                    #кнопки
                    chanchel = 'chanchel_' + f"{call.message.chat.id}_" + f"{orderid}"
                    builder = InlineKeyboardBuilder()
                    builder.button(text = 'Уточнить местонахождение', callback_data = 'test')
                    builder.button(text = 'Отменить заказ', callback_data = chanchel)
                    builder.button(text = 'Главное меню', callback_data = 'menu')
                    builder.adjust(1,1,1)
                    #Отправка сообщение пользователю

                    text = f"\nЗаказ №{orderid} принят" \
                            f"\n{bat_order} бат - {rub} руб" \
                            f"\nКурс:{cur_rub} руб/бат" \
                            "\n"
                    await call.bot.send_message(chat_id = call.message.chat.id, text =text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
                    #Отправка сообщения оператору
                    for result in users.find({'adm': 1}):
                        data = 'message' + f"{call.message.chat.id}"
                        builder = InlineKeyboardBuilder()
                        builder.button(text = 'Взять в работу', callback_data = 'access' + f"{call.message.chat.id}" + f"_{orderid}")
                        builder.adjust(1,1)
                        req = users.find_one({'chatid': call.message.chat.id})
                        request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={call.message.chat.id}")
                        text = f"\nРазместил заказ №{orderid}" \
                                f"\n@{req['username']}" \
                                f"\n{req['FirstName']} {req['LastName']}" \
                                f"\n<code>{call.message.chat.id}</code>" \
                                f"\n{request}" \
                                f"\n{bat_order} бат - {rub} руб" \
                                f"\nКурс:{cur_rub} руб/бат"
                        await call.bot.send_message(chat_id = result['chatid'], text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML',disable_web_page_preview=True)
                        #Создание заказа в дб
                    orderadd = {
                        'orderid': orderid,
                        'bat': bat_order,
                        'fiat': 'bat_rub',
                        'curse': cur_rub,
                        'rub': rub,
                        'date': date,
                        'active': True,
                        'chatid': call.message.chat.id,
                    }
                    yes = order.insert_one(orderadd)
        await call.bot.answer_callback_query(call.id)

#Размещение заказа бат - usdt
@dp.callback_query(lambda c: c.data.startswith('create_order_bat_usdt'))
async def rub(call: types.CallbackQuery,state: FSMContext):
    d = dt.utcnow()
    f = timedelta(hours = 3)
    d = d + f
    for t in temp.find({'chatid': call.message.chat.id}):
        if t['id'] == id and t['fiat'] == 'bat':
            temp.delete_one({'id': id, 'fiat':'bat'})
            await call.bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
            temptime = t['time']
            ordertime = d - temptime
            ordertime = round(ordertime.total_seconds())
            if ordertime > 1800:
                text = 'Время размещения заказа вышло, пожалуйста сделайте новый расчет.'
                builder = InlineKeyboardBuilder().buttons(text = 'Главное меню', callback_data = 'menu')
                await call.bot.send_message(chat_id = call.message.chat.id, text = text, reply_markup = builder.as_markup())
            if ordertime < 1800:
                #Номер заказа
                ord = []
                day = d.strftime("%d")
                year = d.strftime("%Y")
                month = d.strftime("%m")
                date = f"{day}{month}{year}"
                for orders in order.find({ 'date': date}):
                    ord.append(orders)
                orderid = date + f"{len(ord) + 1}"
                #поиск
                adm = const.find_one({'id_id': 1})
                results = users.find_one({'chatid': call.message.chat.id})
                curse = order.find_one({'curseid': 1})
                #Курс
                bat_order = t['bat']
                n = t['n']
                sebes = t['sebes']
                cur_rub = t['curse_rub']
                cur_usdt = t['curse_usdt']
                rub = t['rub']
                usdt = t['usdt']

                #кнопки
                chanchel = 'chanchel_' + f"{call.message.chat.id}_" + f"{orderid}"
                builder = InlineKeyboardBuilder()
                builder.button(text = 'Уточнить местонахождение', callback_data = 'test')
                builder.button(text = 'Отменить заказ', callback_data = chanchel)
                builder.button(text = 'Главное меню', callback_data = 'menu')
                builder.adjust(1,1,1)
                #Отправка сообщение пользователю

                text = f"\nЗаказ №{orderid} принят" \
                        f"\n{bat_order} бат - {usdt} usdt" \
                        f"\nКурс:{cur_usdt} usdt/бат" \
                        "\n"

                await call.bot.send_message(chat_id = call.message.chat.id, text =text, reply_markup = builder.as_markup(), parse_mode= 'HTML')
                #Отправка сообщения оператору
                for result in users.find({'adm': 1}):
                    data = 'message' + f"{call.message.chat.id}"
                    builder = InlineKeyboardBuilder()
                    builder.button(text = 'Взять в работу', callback_data = 'access' + f"{call.message.chat.id}" + f"_{orderid}")
                    builder.adjust(1,1)
                    req = users.find_one({'chatid': call.message.chat.id})
                    request = hlink('Проверить', f"https://t.me/lolsbotcatcherbot?start={call.message.chat.id}")
                    text = f"\nРазместил заказ №{orderid}" \
                            f"\n@{req['username']}" \
                            f"\n{req['FirstName']} {req['LastName']}" \
                            f"\n<code>{call.message.chat.id}</code>" \
                            f"\n{request}" \
                            f"\n{bat_order} бат - {usdt} usdt" \
                            f"\nКурс:{cur_usdt} usdt/бат"
                    await call.bot.send_message(chat_id = result['chatid'], text = text, reply_markup = builder.as_markup(), parse_mode= 'HTML',disable_web_page_preview=True)
                    #Создание заказа в дб
                    orderadd = {
                        'orderid': orderid,
                        'bat': bat_order,
                        'fiat': 'bat_usdt',
                        'curse': cur_rub,
                        'usdt': usdt,
                        'date': date,
                        'chatid': call.message.chat.id,
                    }
                    yes = order.insert_one(orderadd)
        await call.bot.answer_callback_query(call.id)
