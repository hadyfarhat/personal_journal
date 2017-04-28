import datetime

from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash


DATABASE = SqliteDatabase("journal.db")

class User(UserMixin, Model):
    username = CharField(max_length=100, unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    admin = BooleanField(default=False)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ("-joined_at",)


    def create_user(cls, username, email, password, admin=False):
        cls.create(
            username=username,
            email=email,
            password=generate_password_hash(password),
            admin=admin
        )

class Entry(Model):
    title = CharField(max_length=100)
    timestamp = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=1)
    material_learned = TextField()
    resources_to_remember = TextField()


