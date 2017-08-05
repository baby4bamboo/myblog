from ..models import User,Post,Comment,Category
import datetime
from . import main
from .forms import SigninForm,SignupForm,PostForm,CommentForm,CategoryForm
from flask import render_template, redirect, flash, request, url_for, session
from flask.ext.login import login_required, current_user, logout_user, login_fresh, login_user
from flask.ext.login import login_required


@main.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = User.objects(email=session["email"]).first()
    posts = Post.objects()
    return render_template('index.html', user=user,posts=posts)


@main.route("/initdb")
def initdb():
    # As a list to test debug toolbar
    User.objects().delete()  # Removes
    User(email="bayao@cisco.com", password="123", password_hash=User.generate_password_hash("123"), username="Svan Yao",group="subscriber").save()  # Insert
    User(email="yunjie@gmail.com", password="456",  password_hash=User.generate_password_hash("456"),username="Yun Jie",group="subscriber").save()  # Insert
    users = User.objects.all()
    return render_template('initdb.html', users=users)


@main.route("/login" , methods=["GET", "POST"])
def login():
    form = SigninForm()
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


@main.route("/signup" , methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is None:
            User(email=form.email.data, password=form.password.data, password_hash=User.generate_password_hash(form.password.data), username=form.username.data).save()
            return redirect(url_for("main.login"))
        flash(u"该用户已经注册过了，请直接登陆", 'danger')
    return render_template('signup.html',form=form)


@main.route("/post" , methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()
    user = User.objects(email=session["email"]).first()
    form.category.choices = [(c.name, c.name) for c in Category.objects()]
    if form.validate_on_submit():
        title = Post.objects(title=form.title.data).first()
        if title is None:
            post=Post(title=form.title.data, content=form.content.data, tags=[form.tags.data], author_id=user.id,author=user.username,category=request.form.get('category')).save()
            post.update(set__post_id=str(post.id))
            post.update(set__url="http://127.0.0.1:5000/postpage/"+str(post.id))
            return redirect(url_for("main.index"))
    return render_template('post.html', form=form)


@main.route("/mypost", methods=["GET", "POST"])
@login_required
def mypost():
    user = User.objects(email=session["email"]).first()
    posts = Post.objects(author_id=user.id)
    return render_template('mypost.html', user=user,posts=posts)


@main.route("/postpage/<string:page>", methods=["GET", "POST"])
@login_required
def postpage(page=None):
    user = User.objects(email=session["email"]).first()
    post = Post.objects(post_id=page).first()
    comments = Comment.objects(post_id=page)
    if post.author == user.username:
        isauther=True
    else:
        isauther=False
    form = CommentForm()
    if form.validate_on_submit():
        check_comments=Comment.objects(content=form.content.data).first()
        if check_comments is None:
            Comment(content=form.content.data,author=user.username,author_id=user.id,post_id=post.post_id).save()
            form.content.data=""
    return render_template('postpage.html', post=post,user=user,form=form,comments=comments,isauther=isauther)

@main.route("/postpage/<string:page>/edit", methods=["GET", "POST"])
@login_required
def postedit(page=None):
    form = PostForm()
    form.category.choices = [(c.name, c.name) for c in Category.objects()]
    user = User.objects(email=session["email"]).first()
    post = Post.objects(post_id=page).first()
    if form.validate_on_submit():
        post.update(set__title=form.title.data)
        post.update(set__content=form.content.data)
        post.update(set__tags=[form.tags.data])
        post.update(set__category=request.form.get('category'))
        post.update(set__timestamp=datetime.datetime.now)
        return redirect(post.url)
    form.title.data=post.title
    form.content.data=post.content
    form.tags.data=post.tags[0]
    return render_template('post.html', post=post,user=user,form=form)

@main.route("/category" , methods=["GET", "POST"])
@login_required
def category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category.objects(name=form.name.data).first()
        if category is None:
            Category(name=form.name.data, description=form.description.data).save()
            return redirect(url_for("main.index"))
    return render_template('category.html', form=form)


@main.route("/admin" , methods=["GET", "POST"])
@login_required
def admin():
    return render_template('admin.html')


