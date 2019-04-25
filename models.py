from peewee import *

db = SqliteDatabase('softgreen.db')


class Person(Model):
    first_name = CharField()
    last_name = CharField()
    user_id = IntegerField()
    pin_number = IntegerField()

    class Meta:
        database = db


class Administrator(Person):
    pass


class Faculty(Person):
    pass


class Moderator(Person):
    pass


class Semester(Model):
    terms = CharField(unique=True)

    class Meta:
        database = db


class Courses(Model):
    course_code = CharField(unique=True)
    course_name = CharField(unique=True)
    department = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([Person, Administrator, Faculty, Moderator, Semester, Courses])
