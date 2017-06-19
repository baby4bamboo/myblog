# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms.fields.html5 import EmailField, URLField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, HiddenField, BooleanField
from wtforms.validators import InputRequired, Required, Length, Email, Regexp, EqualTo


class SigninForm(Form):
    email = StringField(u"Email")
    password = PasswordField(u"密码")
    remember = BooleanField()
    submit = SubmitField(u"登录")


class SignupForm(Form):
    choices = [
        ("subscriber", u"关注者"),
        ("editor", u"编辑"),
        ("administrator", u"管理员"),
    ]

    email = EmailField(u"邮箱", validators=[InputRequired()])
    username = StringField('昵称', validators=[Required(), Length(1, 64)])
    password = PasswordField(u"密码", validators=[InputRequired(), EqualTo("password2", message="密码不相同")])
    password2 = PasswordField(u"用户密码确认*", validators=[InputRequired()], description=u"请确认你的密码, 与上面输入的密码保持一致.")
    submit = SubmitField(u"确认注册")

class PostForm(Form):
    content_id = HiddenField()
    title = StringField(u"标题", validators=[InputRequired()])
    content = TextAreaField()
    tags = StringField(u"标签")
    submit = SubmitField(u"保存")
