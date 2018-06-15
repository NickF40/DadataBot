from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from base import get_users
from classes import Client


def welcome_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row('Мониторинг', 'Найден')
    markup.row('Информация')
    return markup


def yes_no(id):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Да', callback_data='yes/%d' % id),
               InlineKeyboardButton('Нет', callback_data='no/%d' % id))
    return markup


def error_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Да, ошибся', callback_data='error'),
               InlineKeyboardButton('Передумал мониторить', callback_data='stop'))
    return markup


def delete_user_markup(user_inn):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Удалить', callback_data='delete/%s' % user_inn))
    return markup


def skip_markup(step):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Пропустить', callback_data='skip/%s' % str(step)))
    return markup


def inf_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.row('О Сервисе', 'FAQ')
    markup.row('Список клиентов', 'Назад')
    return markup


def user_list(parent_id, page):
    import pdb
    pdb.set_trace()
    markup = InlineKeyboardMarkup()
    data = get_users(parent_id)[(page - 1) * 10:page * 10]
    for u in data:
        cl = Client(u, t_data=None, parent=None)
        markup.add(InlineKeyboardButton(cl.description(), callback_data='info/%s' % cl.id))
    finrow = []
    if page > 1:
        finrow.append(InlineKeyboardButton('%d<---Назад' % int(page) - 1, callback_data='page/%d' % int(page) - 1))
    if get_users(parent_id)[page * 10:]:
        finrow.append(InlineKeyboardButton('Следующая--->%d' % int(page) + 1, callback_data='page/%d' % int(page) + 1))
    markup.row(*finrow)
    return markup


def edit_markup(uid):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Изменить', callback_data='edit/%s' % str(uid)),
               InlineKeyboardButton('Удалить', callback_data='delete/%s' % str(uid)))
    return markup


"""

def next_page_markup(page_num):
    markup = InlineKeyboardMarkup()
    page_num = int(page_num)
    if page_num == 1:
        markup.row(InlineKeyboardButton('---->', callback_data='page/%s' % str(page_num + 1)))
        return markup
    elif page_num > 1:
        markup.row(InlineKeyboardButton('<----', callback_data='page/%s' % str(page_num - 1)),
                   InlineKeyboardButton('(%s)' % str(page_num), callback_data='-'),
                   InlineKeyboardButton('---->', callback_data='page/%s' % str(page_num + 1)))
        return markup
"""
