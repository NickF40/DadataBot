from base import *


class Client:
    def __init__(self, data, t_data=None, parent=None):
        if data:
            self.id = data[0]
            self.inn = data[1]
            self.name = data[2]
            return
        else:
            inn = t_data.get('inn')
            if t_data.get('type') == 'search':
                data = get_user(inn, parent)
                if not data:
                    self.create_user(inn, parent)
                    data = get_user(inn, parent)
            elif t_data.get('type') == 'new':
                self.isk = t_data.get('isk')
                self.id = t_data.get('id')

            self.inn = inn
            self.name = t_data.get('name')
            self.person = t_data.get('person')
            self.phone = t_data.get('phone')
            self.mail = t_data.get('e-mail')
            self.parent = parent
            return

    @staticmethod
    def create_user(inn, parent):
        new_user(inn, parent)

    def delete(self):
        delete_user(self.inn)
        del self

    def description(self):
        return "%s" % self.name

    def modify(self):
        if 'isk' in self.__dict__.keys():
            set_client(self.inn, self.name, self.person, self.phone, self.mail, self.isk, self.parent, self.id)
            return
        set_user(self.inn, self.name, self.person, self.phone, self.mail, self.parent)
