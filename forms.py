from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, TextField
from wtforms.validators import (DataRequired, Length, Regexp, Email, EqualTo,
                                ValidationError)

import models


def username_exists(form, field):
    if models.User.select().where(models.User.username == field.data).exists():
        raise ValidationError("Username already exists")


def email_exists(form, field):
    if models.User.select().where(models.User.email == field.data).exists():
        raise ValidationError("Email already exists")


class RegisterForm(Form):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=7),
            Regexp(
                r'^[a-zA-Z_0-9]+$',
                message=("Username should contain letters, numbers"
                         ", underscores only")
            ),
            username_exists
        ]
    )
    email = StringField(
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=7),
            EqualTo(
                "confirm_password",
                message="Passwords must match"
            )
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired()
        ]
    )


class LoginForm(Form):
    username = StringField(
        "Username",
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )


class PostForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    time_spent = IntegerField(
        "Time Spent",
        validators=[DataRequired(message="Please enter a valid time")]
    )
    material_learned = TextField("Material Learned",
                                 validators=[DataRequired()])
    resources_to_remember = TextField("Resources To Remember",
                                      validators=[DataRequired()])
    label = StringField("Label",
                        validators=[
                            DataRequired(),
                            Length(max=50)
                        ])
