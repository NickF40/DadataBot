import pymysql.cursors
from configs import db_configs

conn = pymysql.connect(**db_configs)
cur = conn.cursor()


def disconnect(func):
    def wrapper(*args):
        res = func(*args)
        conn.commit()
        return res

    return wrapper


@disconnect
def new_user(inn, parent):
    print('\n\n\nAUCHTUNG!\n\n\n')
    if not inn:
        return
    cur.execute('INSERT INTO users(inn, parent) VALUES (%s, %s)', (inn, str(parent)))


@disconnect
def new_client(inn, parent):
    cur.execute('INSERT INTO users_table(inn, parent) VALUES (%s, %s)',
                (str(inn), str(parent)))
    return get_max_id('clients').get('max(id)')


@disconnect
def set_client(inn, name, person, phone, mail, isk, parent, id):
    # self.inn, self.name, self.person, self.phone, self.mail, self.isk, self.parent, self.id
    cur.execute(
        'UPDATE users_table SET inn = %s, name = %s, person = %s, phone = %s, mail = %s, isk = %s WHERE id = %s',
        (inn, name, person, phone, mail, isk, id))


@disconnect
def delete_client(id_):
    cur.execute('DELETE FROM users_table WHERE id = %s', (id_,))


@disconnect
def get_max_id(table):
    if table == 'users':
        cur.execute('SELECT max(id) from users')
        return cur.fetchone()
    elif table == 'clients':
        cur.execute('SELECT max(id) from users_table')
        return cur.fetchone()


@disconnect
def get_user(inn, parent):
    cur.execute('SELECT * FROM users WHERE inn = %s and parent = %s', (str(inn), str(parent)))
    res = cur.fetchone()
    if not res:
        return None
    res = [res['id'], res['inn'], res['name'], res['person'], res['phone'], res['mail'], res['parent']]
    return res


@disconnect
def set_user(inn, name, person, phone, mail, parent):
    cur.execute('UPDATE users SET name = %s, person = %s, phone = %s, mail = %s where parent = %s and inn = %s',
                (name, person, phone, mail, str(parent), str(inn)))


@disconnect
def delete_user(inn, parent):
    import pdb
    pdb.set_trace()
    cur.execute('DELETE FROM users WHERE inn = %s and parent = %s', (inn, parent))


@disconnect
def get_user_by_id(id_):
    cur.execute('SELECT * FROM users WHERE id = %d' % int(id_))
    return cur.fetchone()


def get_users(parent_id):
    cur.execute('SELECT * FROM users where parent = %s', (parent_id,))
    return [[res['id'], res['inn'], res['name'], res['person'], res['phone'], res['mail'], res['parent']]
            for res in cur.fetchall()]
