
from urllib.parse import quote

from flask import Flask
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import paypalrestsdk
from flask_admin import Admin


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['FLASK_ADMIN_SWATCH'] = 'Solar'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/saleapp?charset=utf8mb4' % quote('12345678')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'


db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Quản trị OU Computer', template_mode='bootstrap4')
login_manager = LoginManager()
login = LoginManager(app=app)
babel = Babel(app=app)


cloudinary.config(
    cloud_name="de3yhowd4",
    api_key="945421312381893",
    api_secret="JbKRQ8KcHDDW9fSYDyYwiq4nmEo",
    secure=True
)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox hoặc live
  "client_id": "ATLpChZkZEMbpjMBfWW4VD0v86yHaMSq3cQ6ePbSn9rU9aTJu_4mf4LiQOT8RWAk8L1iNy3YyU7qPMpy",
  "client_secret": "EOq5Nb3_yZMloN3FwCWNwpPKSZt5KN-ZxY8c33n9Uc48VATADdmLd_mnovsD42PosqrrGUGjED-ECWsV"
})


@babel.localeselector
def load_locale():

    return 'vi'