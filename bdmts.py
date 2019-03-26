import sqlite3
from flask import Flask, render_template, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import PasswordField, BooleanField

app = Flask(__name__)


class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        print(1)
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             name VARCHAR(50),
                             surname VARCHAR(50),
                             email VARCHAR(50),
                             country VARCHAR(50),
                             products VARCHAR(500)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, name, surname, email, country, products):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, name, surname, email, country, products) 
                          VALUES (?,?,?,?,?,?,?)''', (user_name, password_hash, name, surname, email, country, products))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, user1_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user1_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id)))
        cursor.close()
        self.connection.commit()

    def add_product(self, product_id):
        user = self.get(session['user_id'])
        a = (user[7] + ' ' + str(product_id)).strip()
        cursor = self.connection.cursor()
        cursor.execute(
            '''UPDATE users SET products = '{}' WHERE id = {}'''.format(
                a, str(session['user_id'])))
        cursor.close()
        self.connection.commit()

    def clear(self):
        cursor = self.connection.cursor()
        cursor.execute(
            '''UPDATE users SET products = '{}' WHERE id = {}'''.format(
                '', str(session['user_id'])))
        cursor.close()
        self.connection.commit()


class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, content, user_id) 
                          VALUES (?,?,?)''', (title, content, str(user_id),))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id)))
        cursor.close()
        self.connection.commit()


class ProductsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             image VARCHAR(1000),
                             product_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, image, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products
                          (title, content, image, product_id) 
                          VALUES (?,?,?,?)''', (title, content, image, product_id))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return rows

    def delete(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM products WHERE id = ?''', (str(product_id)))
        cursor.close()
        self.connection.commit()


dataBase = DB()
news122 = NewsModel(dataBase.get_connection())
news122.init_table()
k = 0
products_modell = ProductsModel(dataBase.get_connection())
products_modell.init_table()
'''products_modell.insert('Тапочки', 'Теплые и удобные',
                       'https://files.rakuten-static.de/ea731c4266d69e642f191931fcef8206/images/62206a72270b906e2544'
                       'ea4cc11327ee.jpg', k)'''
k += 1
user_model1 = UsersModel(dataBase.get_connection())
user_model1.init_table()
'''user_model1.insert('user', 'pass', 'vas', 'bas', 'aasss', 'rusland', '')'''
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def start():
    form = LoginForm()
    form1 = RegForm()
    if form1.validate_on_submit():
        user_name = form1.username.data
        name = form1.name.data
        surname = form1.surname.data
        password = form1.password.data
        country = form1.country.data
        email = form1.email.data
        user_model1.insert(user_name, password, name, surname, email, country, '')
        exists = user_model1.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/home")
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(dataBase.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/home")
    return render_template('main.html', title='Магазин', form=form, form1=form1)


@app.route('/korzina')
def show_korz():
    products = []
    for i in user_model1.get(session['user_id'])[7].split():
        products.append(products_modell.get(i))
        print(products_modell.get(i))
    return render_template('korz.html', title='Магазин', products=products)


@app.route('/products', methods=['GET', 'POST'])
def show_menu():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(dataBase.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/products")
    form1 = RegForm()
    if form1.validate_on_submit():
        user_name = form1.username.data
        name = form1.name.data
        surname = form1.surname.data
        password = form1.password.data
        country = form1.country.data
        email = form1.email.data
        user_model1.insert(user_name, password, name, surname, email, country, '')
        exists = user_model1.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/products")
    products = products_modell.get_all()
    return render_template('products.html', title='Магазин', form=form, form1=form1, products=products)


@app.route('/profile')
def show_profile():
    return render_template('profile.html', title='Магазин', user=user_model1.get(session['user_id']))


@app.route('/addToKorz/<int:products_id>', methods=['GET'])
def add_to_korz(products_id):
    if 'user_id' in session:
        user_model1.add_product(products_id)
        return redirect('/korzina')
    else:
        return redirect('/home')


@app.route('/clear')
def clear():
    user_model1.clear()
    return redirect('/home')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect("/home")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
