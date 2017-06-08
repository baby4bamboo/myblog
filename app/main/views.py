from ..models import Todo,User
from . import main
from .forms import LoginForm,RegistrationForm
from flask import render_template, redirect, flash, request, url_for, session
from flask.ext.login import login_required, current_user, logout_user, login_fresh, login_user
from mongoengine import NotUniqueError
from flask.ext.login import login_required


@main.route("/", methods=["GET", "POST"])
@login_required
def index():
    # As a list to test debug toolbar
    Todo.objects().delete()  # Removes
    Todo(title="Simple todo A", text="12345678910").save()  # Insert
    Todo(title="Simple todo B", text="12345678910").save()  # Insert
    Todo.objects(title__contains="B").update(set__text="Hello world")  # Update
    todos = list(Todo.objects[:10])
    todos = Todo.objects.all()
    return render_template('index.html', todos=todos)


@main.route("/user")
def user():
    # As a list to test debug toolbar
    User.objects().delete()  # Removes
    User(email="bayao@cisco.com", password="123", password_hash=User.generate_password_hash("123"), username="Svan Yao",group="subscriber").save()  # Insert
    User(email="yunjie@gmail.com", password="456",  password_hash=User.generate_password_hash("456"),username="Yun Jie",group="subscriber").save()  # Insert
    users = User.objects.all()
    return render_template('user.html', users=users)


@main.route("/pagination")
@login_required
def pagination():
    Todo.objects().delete()
    for i in range(10):
        Todo(title='Simple todo {}'.format(i), text="12345678910").save()  # Insert

    page_num = int(request.args.get('page') or 1)
    todos_page = Todo.objects.paginate(page=page_num, per_page=3)

    return render_template('pagination.html', todos_page=todos_page)

@main.route("/login" , methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            session["email"] = user.email
            login_user(user, form.remember)
            return redirect(url_for("main.index"))
        flash(u"用户名或密码错误", 'danger')
    return render_template('login.html',form=form)

@main.route("/logout")
@login_required
def logout():
    session["email"] = None
    logout_user()
    flash(u"您已经退出登录", 'success')
    return redirect(url_for("main.login"))

@main.route("/register" , methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is None:
            User(email=form.email.data, password=form.password.data,password_hash=User.generate_password_hash(form.password.data),username=form.username.data,group=form.group.data).save()
            return redirect(url_for("main.login"))
        flash(u"该用户已经注册过了，请直接登陆", 'danger')
    return render_template('register.html',form=form)
