from flask import Flask, Response, send_from_directory

from flask_admin.contrib.sqla import ModelView

from flask_basicauth import BasicAuth

from flask import render_template

from flask_admin import Admin, AdminIndexView, expose

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String

from werkzeug.exceptions import HTTPException

from werkzeug.utils import redirect



# create an app and define basic authentication

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'set any username you want'

app.config['BASIC_AUTH_PASSWORD'] = 'set any password you want'



basic_auth = BasicAuth(app)





# some classes to make BasicAuth work with flask-admin

class AuthException(HTTPException):

    def __init__(self, message):

        super().__init__(message, Response(

            "Не получилось авторизоваться. Обновите страницу и попробуйте ещё раз", 401,

            {'WWW-Authenticate': 'Basic realm="Login Required"'}))





class MyModelView(ModelView):

    def is_accessible(self):

        if not basic_auth.authenticate():

            raise AuthException('Вы не авторизованы')

        else:

            return True



    def inaccessible_callback(self, name, **kwargs):

        return redirect(basic_auth.challenge())





class MyAdminIndexView(AdminIndexView):

    @expose('/')

    def index(self):

        return self.render('auth.html', db=db,

                           Maslenitsa=Maslenitsa,

                           Sabantuy=Sabantuy)



    def is_accessible(self):

        if not basic_auth.authenticate():

            raise AuthException('Вы не авторизованы')

        else:

            return True



    def inaccessible_callback(self, name, **kwargs):

        return redirect(basic_auth.challenge())





# initialize the database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'

app.config['SECRET_KEY'] = b'\x01\xabF\xc3\xa7s\xb2(g\x901\x0ch\xa3\x85\xbe'

db = SQLAlchemy(app)





class Maslenitsa(db.Model):

    __tablename__ = 'moscow_maslenitsa'

    id = Column(Integer(), primary_key=True)

    address = Column(String(65535), nullable=False)

    year = Column(Integer(), nullable=False)

    participants = Column(String(65535), nullable=False)

    form = Column(String(65535), nullable=False)

    contents = Column(String(65535), nullable=False)





maslenitsa = Maslenitsa()





class Sabantuy(db.Model):

    __tablename__ = 'moscow_sabantuy'

    id = Column(Integer(), primary_key=True)

    year = Column(Integer(), nullable=False)

    participants = Column(String(65535), nullable=False)

    form = Column(String(65535), nullable=False)

    contents = Column(String(65535), nullable=False)





sabantuy = Sabantuy()





# initialize flask-admin

app.config['FLASK_ADMIN_SWATCH'] = 'slate'

admin = Admin(app, name='Фольклор 2.0', template_mode='bootstrap3', index_view=MyAdminIndexView())

admin.add_view(MyModelView(Maslenitsa, db.session))

admin.add_view(MyModelView(Sabantuy, db.session))





@app.route('/static/css/<path:path>')

def send_css(path):

    return send_from_directory('static/css', path)





# main page

@app.route('/')

def hi_page():

    return render_template('index.html')





# about the paper

@app.route('/about/')

def about():

    return render_template('about.html')





# general info about the events

@app.route('/general/')

def general():

    return render_template('1.html')





# Московская Масленица

@app.route('/moscow_maslenitsa/')

def masl():

    return render_template('2.html', db=db, Maslenitsa=Maslenitsa)





# Московский Сабантуй

@app.route('/sabantuy/')

def saba():

    return render_template('4.html', db=db, Sabantuy=Sabantuy)





#Выводы

@app.route('/conclusion/')

def conc():

    return render_template('conclusion.html')


# Интерактивная карта

@app.route('/interactive_map/')

def interactive_map():

    return render_template('map1.html')