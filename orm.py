import sqlite3
import logging

logging.basicConfig(level=logging.INFO)


class SqliteORM(object):

    def __init__(self, *args, **kwargs):
        self._model = self.__class__.__name__
        self._columns = {column for column in self.__class__.__dict__.keys() if not column.startswith('__')}
        self._query = None
        self.connect = None

    @staticmethod
    def fields_list(fields):
        return ', '.join(fields)

    def connect_to(self, name_db):
        try:
            con = sqlite3.connect(name_db)
        except Exception as e:
            logging.info(e)
            raise e
        else:
            self.connect = con

    def create_table(self):
        fields = [f'{field} {getattr(self, field)}' for field in self._columns]
        try:
            cursor = self.connect.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self._model} ({self.fields_list(fields)})')
        except Exception as e:
            logging.info(e)

    def delete_table(self):
        try:
            cursor = self.connect.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS {self._model}')
        except Exception as e:
            logging.info(e)

    def execute(self):
        cursor = self.connect.cursor()
        try:
            cursor.execute(self._query)
            self.connect.commit()
        except Exception as e:
            logging.info(e)
        return cursor.fetchall()

    def get(self, *args):
        self._query = f'SELECT {self.fields_list(args or self._columns)} FROM {self._model}'
        return self

    def create(self, **kwargs):
        fields = self.fields_list(kwargs.keys())
        values = self.fields_list(map(lambda value: f'"{value}"', kwargs.values()))
        self._query = f"INSERT INTO {self._model} ({fields}) VALUES ({values})"
        return self

    def update(self, **kwargs):
        fields = self.fields_list([f"{key} = '{value}'" for key, value in kwargs.items()])
        self._query = f'UPDATE {self._model} SET {fields}'
        return self

    def filter(self, field, value, comparison='='):
        self._query = f'{self._query} WHERE {field} {comparison} {value}'
        return self

    def delete(self):
        self._query = f'DELETE FROM {self._model}'
        return self
