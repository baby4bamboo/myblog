# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms.fields.html5 import EmailField, URLField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, HiddenField, BooleanField
from wtforms.validators import InputRequired, Required, Length, Email, Regexp, EqualTo


class LoginForm(Form):
    username = StringField(u"用户名")
    password = PasswordField(u"密码")
    remember = BooleanField()
    submit = SubmitField(u"登录")
