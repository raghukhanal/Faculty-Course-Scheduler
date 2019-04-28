from peewee import *

db = SqliteDatabase('softgreen.db')


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()
    user_id = IntegerField(unique=True)
    pin_number = IntegerField()
    FT_PT = (
        (1, "FT"),
        (2, "PT")
    )
    ft_pt = IntegerField(choices=FT_PT)


class Administrator(Person):
    pass


class Faculty(Person):
    pass


class Moderator(Person):
    pass


class ClassRoom(BaseModel):
    room = CharField(unique=True)


class Semester(BaseModel):
    terms = CharField(unique=True)


class Courses(BaseModel):
    course_code = CharField()
    course_name = CharField()
    course_section = IntegerField()

    credit = IntegerField()

    notes = CharField(null=True)
    tom_notes = CharField(null=True)


class DayTime(BaseModel):
    courses = ForeignKeyField(Courses, backref="day_time")
    days = CharField()
    start_time = CharField()
    end_time = CharField()
    class_room = ManyToManyField(ClassRoom)


class SelectedCourseInfo(BaseModel):
    faculty = ForeignKeyField(Faculty, backref="selected_course")
    course = ForeignKeyField(Courses, backref="selected_course")


db.connect()
db.create_tables([Person, Administrator, Faculty, Moderator, Semester, Courses, DayTime, ClassRoom, SelectedCourseInfo])
