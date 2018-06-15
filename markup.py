from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


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
    markup.row('Список клиентов')
    return markup
  
def next_page_markup(page_num):
  markup = InlineKeyboardMarkup() 
  if page_num == 1:
    markup.row(InlineKeyboardButton('---->', callback_data='page/%s' % str(page_num+1)))
    return markup
  elif page_num > 1:
    markup.row(InlineKeyboardButton('<----', callback_data='page/%s' % str(page_num-1)),
    InlineKeyboardButton('(%s)' % str(page_num), callback_data='-') ,
    InlineKeyboardButton('---->', callback_data='page/%s' % str(page_num+1)))
    return markup
      
   
    
    