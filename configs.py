import pymysql

welcome_text = "Привет!"
mon_text = 'Введите ИНН компании или индивидуального предпринимателя, которого нужно мониторить'
mon_text_2 = 'За этим мониторим?'
mon_text_3 = 'Введите контакты клиента'
mon_text_4 = 'Вы ошиблись в ИНН? Или передумали мониторить за ним?' 
mon_error_text = 'Не могу найти такой ИНН в ЕГРЮЛ, проверьте корректность и повторите попытку отправки на Мониторинг'
new_text_2 = 'Как только появится, заводите'
main_menu_text = 'Это текст главного меню'


error_text = 'Проверьте правильность ИНН и повторите попытку отправки на Мониторинг'
stop_mon_text = 'Понял, не буду мониторить за ним.'
confirm_message = 'ОК, зафиксировал'
lines = ['Контактное лицо', 'Электронная почта', 'Телефон']
error_message = 'Ошибка! Неверное написание '
modification_text = "text"
modification_text_2 = "text2"
modification_text_3 = 'Succesfully!'

new_client_text_1 = 'У Вас есть Клиент'
# if information - only message
# information = ''

# elif information - array of messages
information = ['Тут инфа о сервисе', 'Тут часто задаваемые вопросы']
# ----------

# replace if needed
user_lines = ['inn', 'name']

"""

"""

db_configs = dict(host='', user='', password='', db='', charset='utf8mb4',
                  cursorclass=pymysql.cursors.DictCursor)

# constants
TOKEN = ''

# if needed to form invite link
# BOTNAME = ''
# URL = "https://t.me/"+BOTNAME+'?start='
# LINK = "https://t.me/"+BOTNAME

WEBHOOK_HOST = '256.256.256.256'            # Host IP
WEBHOOK_PORT = 443                          # Any free
WEBHOOK_LISTEN = ''          # Host IP

WEBHOOK_SSL_CERTIFICATE = 'webhook_cert.pem'  # Ssl certificate path
WEBHOOK_SSL_PRIVATE_KEY = 'webhook_pkey.pem'  # Ssl private key path

# May be changed to any other path
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % TOKEN
WEBHOOK_URL_BASE2 = "http://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)

