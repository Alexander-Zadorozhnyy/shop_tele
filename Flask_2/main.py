from flask import Flask, render_template, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Flask_2.data import db_session
from Flask_2.data.basket import Basket
from Flask_2.data.category import Category, category_to_items
from Flask_2.data.commands import create_item, create_basket, edit_item, delete_item
from Flask_2.data.support_question import Questions
from Flask_2.data.theme_questions import Themes
from Flask_2.data.users import User
from Flask_2.data.shop_items import Items
from Flask_2.forms.user import RegisterForm, SupportForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
questions = []
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/shop_info.db")
    db_sess = db_session.create_session()
    '''create_item(content='samsung_a40.jpeg', name='Xiaomi_tablet', about='Планшет')'''
    '''edit_item(1, content='iphone_10.jpg')
    edit_item(2, content='iphone_11.jpg')
    edit_item(3, content='samsung_s10.jpeg', name='Samsung S10')
    edit_item(4, content='samsung_a40.jpeg', name='Samsung A40')
    edit_item(5, content='xiaomi_redmi_8a.jpg', name='Xiaomi Redmi 8A')'''

    app.run(debug=True)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    item = Items
    items = [str(item).split('-') for item in db_sess.query(Items).all()]
    print(items)
    all_types = ['bg-dark me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-primary me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden'
                 ]
    return render_template("index.html", count=len(items), all_types=all_types, items=items)  # , items=items


@app.route('/support', methods=['GET', 'POST'])
def support():
    form = SupportForm()
    db_sess = db_session.create_session()
    form.theme.choices = [(theme.id, theme.theme) for theme in db_sess.query(Themes).all()]
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.email == form.email.data).first():
            question = Questions(question=form.question.data, user_id=db_sess.query(User.id).filter(User.email == form.email.data).first()[0],
                                 theme_id=form.theme.data)
            db_sess.add(question)
            db_sess.commit()
            flash("Ваш запрос успешно отправлен в тех.поддержку", "success")
        else:
            return render_template('support.html', title='Поддержка',
                                       form=form,
                                       message="Пользователя с таким email не существует")
        return redirect('/index')
    return render_template('support.html', title='Поддержка', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/tablets')
def tablets_page():
    db_sess = db_session.create_session()
    items = [str(item).split('-') for item in db_sess.query(Items).filter(category_to_items.c.category == 1).all()]
    all_types = ['bg-dark me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-primary me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden'
                 ]
    return render_template("index.html", count=len(items), all_types=all_types, items=items)


@app.route('/phones')
def phones_page():
    db_sess = db_session.create_session()
    # Нужно переименовать название items на item в category_to_items
    print([item for item in db_sess.query(category_to_items.c.item).all()])
    items_note = [str(item).split('-') for item in db_sess.query(Items.id).filter(category_to_items.c.category == 2).all()]
    print(items_note)
    all_types = ['bg-dark me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-primary me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center text-white overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden',
                 'bg-light me-md-3 pt-3 px-3 pt-md-5 px-md-5 text-center overflow-hidden'
                 ]
    return render_template("index.html", count=len(items), all_types=all_types, items=items)


if __name__ == '__main__':
    main()
