from orm import SqliteORM


class User(SqliteORM):
    id = 'int'
    name = 'str'
    age = 'int'
    email = 'str'


# create new user and testing different methods
user = User()
user.connect_to("db.sqlite3")
user.create_table()
print('table User is created')

user.create(id=1, name='Steve', email='steve@mail.ru', age=41).execute()
user.create(id=2, name='Bill', email='bill@mail.ru').execute()
user.create(id=3, name='John', email='john@mail.ru', age=33).execute()
result = user.get('name', 'email', 'age').execute()
print(f'Users created with result: {result}')

user.update(name="Elon").filter('id', 1).execute()
result = user.get().filter('id', 1).execute()
print(f'User with id 1 updated name to "Elon",  result: {result}')

user.delete().filter('id', 2).execute()
result = user.get('name', 'email', 'age').execute()
print(f'User with id 2 is deleted. Result: {result}')

user.delete_table()
print('table User is deleted')
