# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms.fields.html5 import EmailField, URLField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, HiddenField, BooleanField
from wtforms.validators import InputRequired, Required, Length, Email, Regexp, EqualTo


class LoginForm(Form):
    email = StringField(u"Email")
    password = PasswordField(u"密码")
    remember = BooleanField()
    submit = SubmitField(u"登录")


class RegistrationForm(Form):
    email = EmailField(u"邮箱", validators=[InputRequired()])
    username = StringField('用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, ''numbers, dots or underscores')])
    password = PasswordField(u"密码", validators=[InputRequired(), EqualTo("password2", message="密码不相同")])
    password2 = PasswordField(u"用户密码确认*", validators=[InputRequired()], description=u"请确认你的密码, 与上面输入的密码保持一致.")
    submit = SubmitField(u"确认注册")
