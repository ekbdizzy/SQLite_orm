## Simple ORM for SQLite
~~~
from orm import SqliteORM
~~~ 

### Sample creating model:
~~~
class User(SqliteORM):
    id = 'int'
    name = 'str'
    age = 'int'
    email = 'str'

model = Model()
user.connect_to("db.sqlite3")
user.create_table()
~~~

### Methods of model:
~~~
# create instance
model.create(**fields).execute()

# update fields of model
model.update(**fields).execute()

# get objects by fields
model.get(**field).execute()

# get object by filter
model.get().filter(field, value, comparison=equal).execute()
model.delete() 

# delete object by filter
user.delete().filter(field, value).execute()
~~~





