import datetime

# NOTE
# pep8 will throw errors because of the below line
# but this is the convention we should use ...
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

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        cls.create(
            username=username,
            email=email,
            password=generate_password_hash(password),
            admin=admin
        )


class Label(Model):
    content = CharField(max_length=50)

    class Meta:
        database = DATABASE


class Entry(Model):
    title = CharField(max_length=100)
    timestamp = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField(default=1)
    material_learned = TextField()
    resources_to_remember = TextField()
    user = ForeignKeyField(
        rel_model=User,
        related_name="entries"
    )
    label = ForeignKeyField(
        rel_model=Label,
        related_name="entries"
    )

    class Meta:
        database = DATABASE
        order_by = ("-timestamp",)


def initialize():
    DATABASE.connect()
    # DATABASE.drop_tables([User, Label, Entry])
    DATABASE.create_tables([User, Label, Entry], safe=True)
    DATABASE.close()
