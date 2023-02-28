from SaleApp import utils
from flask_admin import Admin, BaseView, expose, AdminIndexView

from SaleApp.init import app
from SaleApp.models import *
from flask_admin.contrib.sqla import ModelView
from flask import request, render_template, redirect, url_for
from flask_login import current_user, logout_user

# admin = Admin(app=app, name="Quản trị khách sạn", template_mode='bootstrap4')
app.secret_key = '#@!$%^#$^$#!@%$@#$^%*&^%dsad!2321321r%^%$&^%Sfdfds'


admin = Admin(app=app, name='Quản trị khách sạn', template_mode='bootstrap4')

