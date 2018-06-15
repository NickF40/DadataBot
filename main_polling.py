import telebot
from configs import *
from markups import *
from dadata import suggest
import re
from classes import *

bot = telebot.TeleBot(TOKEN)

# memcached!!!
temp_data = {}

phone_regexp = re.compile(r"^((\+7|7|8)+([0-9]){10})$")
mail_regexp = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def get_phone(message):
    import pdb
    pdb.set_trace()
    temp_data[message.chat.id].update({'phone': message.text})
    data = temp_data[message.chat.id]
    if data.get('type') == 'new':
        bot.send_message(message.chat.id, 'Отправить адвокату?\n\n'
                                          'Клиент: %s\n'
                                          'ИНН: %s\n'
                                          'Сумма иска: %s\n'
                                          'Контактное лицо: %s\n'
                                          'Телефон: %s\n'
                                          'Мыло: %s' % (data.get('name'), data.get('inn'), data.get('isk'),
                                                        data.get('person'), data.get('phone'), data.get('e-mail')),
                         reply_markup=yes_no(5))
        return
    client = Client(None, t_data=temp_data[message.chat.id], parent=message.chat.id)
    client.modify()
    del temp_data[message.chat.id]
    bot.send_message(message.chat.id, confirm_message, reply_markup=welcome_markup())
    return


def get_mail(message):
    temp_data[message.chat.id].update({"e-mail": message.text})
    msg = bot.send_message(message.chat.id, lines[2], reply_markup=skip_markup(2))
    bot.clear_step_handler(msg)
    bot.register_next_step_handler(msg, get_phone)
    return


def get_person(message):
    if not message.chat.id in temp_data.keys():
        temp_data[message.chat.id] = {'person': message.text}
    else:
        temp_data[message.chat.id].update({'person': message.text})
    msg = bot.send_message(message.chat.id, lines[1], reply_markup=skip_markup(1))
    bot.clear_step_handler(msg)
    bot.register_next_step_handler(msg, get_mail)
    return


# data + inn verification
def handle_inn(message):
    if message.text == 'Мониторинг':
        handle_monitoring(message)
        return
    elif message.text == 'Найден':
        found_handler(message)
        return
    elif message.text == 'Информация':
        handle_information(message)
        return

    result = suggest(message.text, 'party')
    if not result or not message.text.isdigit():
        msg = bot.send_message(message.chat.id, mon_error_text)
        bot.clear_step_handler(msg)
        return

    if message.chat.id in temp_data.keys():
        temp_data[message.chat.id].update({'inn': message.text})
    else:
        temp_data[message.chat.id] = {"inn": message.text}
    temp_data[message.chat.id].update({'name': result[0], 'type': 'search'})
    bot.send_message(message.chat.id, mon_text_2)
    bot.send_message(message.chat.id, "Компания: " + result[0], reply_markup=yes_no(0))


def get_inn(message):
    if message.text == 'Мониторинг':
        handle_monitoring(message)
        return
    elif message.text == 'Найден':
        found_handler(message)
        return
    elif message.text == 'Информация':
        handle_information(message)
        return

    result = suggest(message.text, 'party')
    if not result or not message.text.isdigit():
        msg = bot.send_message(message.chat.id, mon_error_text)
        bot.clear_step_handler(msg)
        return
    if message.chat.id in temp_data.keys():
        temp_data[message.chat.id].update({'inn': message.text})
    else:
        temp_data[message.chat.id] = {"inn": message.text}
    temp_data[message.chat.id].update({'name': result[0], 'type': 'new'})
    bot.send_message(message.chat.id, mon_text_2)
    bot.send_message(message.chat.id, "Компания: " + result[0], reply_markup=yes_no(3))


def get_isk(message):
    if not temp_data[message.chat.id]:
        temp_data[message.chat.id] = {'isk': message.text}
    else:
        temp_data[message.chat.id].update({'isk': message.text})
    msg = bot.send_message(message.chat.id, lines[0], reply_markup=skip_markup(0))
    bot.clear_step_handler(msg)

    bot.register_next_step_handler(msg, get_person)


def form_page(page_num, parent):
    if page_num < 1:
        return
    c = 0
    users = []
    for u in get_users(parent_id=parent):
        if c >= (page_num - 1) * 10:
            if c < page_num * 10:
                users.append(u)
                c += 1
            else:
                return users
        else:
            c += 1
    return users


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, welcome_text, reply_markup=welcome_markup())


@bot.message_handler(regexp=r'Мониторинг')
def handle_monitoring(message):
    msg = bot.send_message(message.chat.id, mon_text)
    bot.clear_step_handler(msg)
    bot.register_next_step_handler(msg, handle_inn)  # ask for inn


@bot.message_handler(regexp=r'Информация')
def handle_information(message):
    bot.send_message(message.chat.id,
                     'Здесь вы можете найти интересующую вас информацию.\nВыберите один из разделов...',
                     reply_markup=inf_markup())


@bot.message_handler(regexp=r'О Сервисе')
def about_service(message):
    bot.send_message(message.chat.id, information[0])


@bot.message_handler(regexp=r'FAQ')
def about_faq(message):
    bot.send_message(message.chat.id, information[1])


@bot.message_handler(regexp=r'Назад')
def step_back(message):
    bot.send_message(message.chat.id, main_menu_text, reply_markup=welcome_markup())


@bot.message_handler(regexp=r'Список клиентов')
def client_list(message):
    npage = user_list(message.chat.id, 1)
    bot.send_message(message.chat.id, 'Следующая страница', reply_markup=npage)


@bot.message_handler(regexp=r'Найден')
def found_handler(message):
    msg = bot.send_message(message.chat.id, new_client_text_1, reply_markup=yes_no(2))
    bot.clear_step_handler(msg)


@bot.callback_query_handler(func=lambda call: call.data.startswith('info'))
def handle_info_query(call):
    import pdb
    pdb.set_trace()
    uid = int(call.data.split('/')[1])
    data = get_user_by_id(uid)
    bot.send_message(call.message.chat.id, 'Клиент: %s\n'
                                           'ИНН: %s\n'
                                           'Контактное лицо: %s\n'
                                           'Телефон: %s\n'
                                           'Мыло: %s' % (data.get('name'), data.get('inn'),
                                                         data.get('person'), data.get('phone'), data.get('mail')),
                     reply_markup=edit_markup(data.get('id')))


@bot.callback_query_handler(func=lambda call: call.data.startswith('page'))
def newx_page_handler(call):
    page_num = call.data.split('/')[1]
    npage = user_list(call.message.chat.id, int(page_num))
    bot.send_message('Следующая страница', reply_markup=npage)


@bot.callback_query_handler(func=lambda call: call.data.startswith('skip'))
def skip_step_handler(call):
    if call.message.chat.id not in temp_data.keys():
        return
    step = int(call.data.split('/')[1])

    # skip phone
    if step == 2:
        temp_data[call.message.chat.id].update({'phone': 'Не указано'})
        if temp_data[call.message.chat.id].get('type') == 'new':
            data = temp_data[call.message.chat.id]
            bot.send_message(call.message.chat.id, 'Отправить адвокату?\n\n'
                                                   'Клиент: %s\n'
                                                   'ИНН: %s\n'
                                                   'Сумма иска: %s\n'
                                                   'Контактное лицо: %s\n'
                                                   'Телефон: %s\n'
                                                   'Мыло: %s' % (data.get('name'), data.get('inn'), data.get('isk'),
                                                                 data.get('person'), data.get('phone'),
                                                                 data.get('e-mail')),
                             reply_markup=yes_no(5))
            return
        message = call.message
        client = Client(None, t_data=temp_data[call.message.chat.id], parent=message.chat.id)
        client.modify()
        del temp_data[message.chat.id]
        msg = bot.send_message(message.chat.id, confirm_message, reply_markup=welcome_markup())
        bot.clear_step_handler(msg)
        return
    # after isk "find"
    elif step == 4:
        temp_data[call.message.chat.id].update({'isk': ' Не указано'})
        msg = bot.send_message(call.message.chat.id, lines[0], reply_markup=skip_markup(0))
        bot.clear_step_handler(msg)
        bot.register_next_step_handler(msg, get_person)
        return

    msg = bot.send_message(call.message.chat.id, lines[int(step) + 1], reply_markup=skip_markup(int(step) + 1))
    bot.clear_step_handler(msg)

    if step == 0:
        temp_data[call.message.chat.id].update({'person': ' Не указано'})
        bot.register_next_step_handler(msg, get_mail)
    elif step == 1:
        temp_data[call.message.chat.id].update({'e-mail': ' Не указано'})
        bot.register_next_step_handler(msg, get_phone)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit'))
def edit_user_query(call):
    uid = call.data.split('/')[1]
    data = get_user_by_id(uid)
    temp_data[call.message.chat.id] = {'type': 'search', 'inn': data.get('inn'), 'name': data.get('name')}
    msg = bot.send_message(call.message.chat.id, lines[0], reply_markup=skip_markup(0))
    bot.clear_step_handler(msg)
    bot.register_next_step_handler(msg, get_person)
    return


@bot.callback_query_handler(func=lambda call: not call.data.startswith('delete') and call.data != '-')
def handle_callback(call):
    if call.data.count('/') == 0:
        if call.data == 'error':
            msg = bot.send_message(call.message.chat.id, mon_text)
            bot.register_next_step_handler(msg, handle_inn)
        elif call.data == 'stop':
            bot.send_message(call.message.chat.id, stop_mon_text)
    else:
        res, step = map(str, call.data.split('/'))
        # company confirmed "trace"
        if step == '0':
            if res == 'yes':
                if not get_user(temp_data[call.message.chat.id].get('inn'), call.message.chat.id):
                    new_user(temp_data[call.message.chat.id].get('inn'), call.message.chat.id)
                bot.send_message(call.message.chat.id, mon_text_3, reply_markup=yes_no(1))
            else:
                del temp_data[call.message.chat.id]
                bot.send_message(call.message.chat.id, error_text, reply_markup=None)
        # redirect to "trace" input seq
        elif step == '1':
            if res == 'yes':
                msg = bot.send_message(call.message.chat.id, lines[0], reply_markup=skip_markup(0))
                bot.clear_step_handler(msg)
                bot.register_next_step_handler(msg, get_person)
            else:
                temp_data[call.message.chat.id].update({'person': 'Не указано',
                                                        'phone': 'Не указано',
                                                        'e-mail': 'Не указано'})
                cl = Client(None, temp_data[call.message.chat.id], call.message.chat.id)
                cl.modify()
                bot.send_message(call.message.chat.id, confirm_message)
        # after "any new clients?"
        elif step == '2':
            if res == 'yes':
                msg = bot.send_message(call.message.chat.id, 'Введите ИНН нового клиента', reply_markup=None)
                bot.clear_step_handler(msg)
                bot.register_next_step_handler(msg, get_inn)
            else:
                msg = bot.send_message(call.message.chat.id, new_text_2)
                bot.clear_step_handler(msg)
        # company confirmed "new"
        elif step == '3':
            if res == 'yes':
                if call.message.chat.id not in temp_data.keys():
                    msg = bot.send_message(call.message.chat.id, 'Что-то пошло не так! Введите ИНН ещё раз!')
                    bot.register_next_step_handler(msg, get_inn)
                    return
                id = new_client(temp_data[call.message.chat.id].get('inn'), call.message.chat.id)
                temp_data[call.message.chat.id].update({'id': id})
                msg = bot.send_message(call.message.chat.id, 'Сумма иска', reply_markup=skip_markup(4))
                bot.clear_step_handler(msg)
                bot.register_next_step_handler(msg, get_isk)
                return
            else:
                msg = bot.send_message(call.message.chat.id, error_text)
                bot.clear_step_handler(msg)
        elif step == '5':
            if res == 'yes':
                cl = Client(None, temp_data[call.message.chat.id], parent=call.message.chat.id)
                cl.modify()
                bot.send_message(call.message.chat.id, confirm_message, reply_markup=welcome_markup())
                return
            else:
                import pdb
                pdb.set_trace()
                delete_client(temp_data[call.message.chat.id].get('id'))
                del temp_data[call.message.chat.id]
                msg = bot.send_message(call.message.chat.id, 'Зачем, Карл?!')
                bot.clear_step_handler(msg)
                return
        else:
            raise Exception('Expected step <=1, got %s' % str(step))


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete'))
def del_user(call):
    inn = call.data.split('/')[1]
    delete_user(inn, call.message.chat.id)
    bot.send_message(call.message.chat.id, confirm_message)


bot.polling(none_stop=True)
