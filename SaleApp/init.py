from urllib.parse import quote

from flask import Flask
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
import cloudinary

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'
app.config['FLASK_ADMIN_SWATCH'] = 'Solar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/saleapp?charset=utf8mb4' % quote('1234')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'
app.config['SO_LUONG_NHAP'] = 150
app.config['SO_LUONG_Ton'] = 300

db = SQLAlchemy(app=app)
login_manager = LoginManager()
login = LoginManager(app=app)
babel = Babel(app=app)

cloudinary.config(
    cloud_name="de3yhowd4",
    api_key="945421312381893",
    api_secret="JbKRQ8KcHDDW9fSYDyYwiq4nmEo",
    secure=True
)


@babel.localeselector
def load_locale():
    return 'vi'