import pymysql as pg
from configs import db_configs

con = pg.connect(**db_configs)
cur = con.cursor()

cur.execute('CREATE TABLE users(id SERIAL PRIMARY KEY, inn TEXT, name TEXT, person TEXT,'
            ' phone TEXT, mail TEXT, parent TEXT)')
cur.execute('CREATE TABLE users_table(id SERIAL PRIMARY KEY, inn TEXT, name TEXT, person TEXT, isk TEXT,'
            ' phone TEXT, mail TEXT, parent TEXT)')
con.commit()
con.close()
