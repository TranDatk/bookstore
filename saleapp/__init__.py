from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary


app = Flask(__name__)
app.secret_key = '4567890sdfghjklcvbnvb4567fg6yug'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/dbnhasach?charset=utf8mb4' % quote('25052002')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(cloud_name='dcyzg2k36', api_key='165436845965685', api_secret='jfjTMPoUDBH54mnmlBSEBG3LENg', api_proxy = "http://proxy.server:3128")

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return "vi"
