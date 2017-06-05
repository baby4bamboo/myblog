import flask
from ..models import Todo,User
from . import main

@main.route("/")
def index():
    # As a list to test debug toolbar
    Todo.objects().delete()  # Removes
    Todo(title="Simple todo A", text="12345678910").save()  # Insert
    Todo(title="Simple todo B", text="12345678910").save()  # Insert
    Todo.objects(title__contains="B").update(set__text="Hello world")  # Update
    todos = list(Todo.objects[:10])
    todos = Todo.objects.all()
    return flask.render_template('index.html', todos=todos)

@main.route("/user")
def user():
    # As a list to test debug toolbar
    User.objects().delete()  # Removes
    User(username="Svan Yao", password="123").save()  # Insert
    User(username="Yun Jie", password="456").save()  # Insert
    users = User.objects.all()
    return flask.render_template('user.html', users=users)


@main.route("/pagination")
def pagination():
    Todo.objects().delete()
    for i in range(10):
        Todo(title='Simple todo {}'.format(i), text="12345678910").save()  # Insert

    page_num = int(flask.request.args.get('page') or 1)
    todos_page = Todo.objects.paginate(page=page_num, per_page=3)

    return flask.render_template('pagination.html', todos_page=todos_page)
