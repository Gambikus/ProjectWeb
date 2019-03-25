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
        a = user[7] + ' ' + str(product_id)
        self.delete(session['user_id'])
        self.insert(user[1], user[2], user[3], user[4], user[5], user[6], a.strip())
        session.pop('user_id', 0)
        session['user_id'] = self.exists(user[1], user[2])[1]

    def clear(self):
        user = self.get(session['user_id'])
        a = ''
        self.delete(session['user_id'])
        if not self.exists(user[1], user[2])[0]:
            self.insert(user[1], user[2], user[3], user[4], user[5], user[6], a.strip())
            session.pop('user_id', 0)
            session['user_id'] = self.exists(user[1], user[2])[1]


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
'''products_modell.insert('Кеды Oliver Sweeney', 'Высококачественная обувь, сделанная из натуральной кожи. '
                                              'В её подовшу встроены пружины, '
                                              'которые обеспечивают комфорт во время ходьбы',
                       'https://static.mainlinemenswear.co.uk/images/header/aw18-oliver-sweeney-banner.jpg', k)'''
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


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def start():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(dataBase.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/home")
    return render_template('main.html', title='Магазин', form=form)


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
    products = products_modell.get_all()
    return render_template('products.html', title='Магазин', form=form, products=products)


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
