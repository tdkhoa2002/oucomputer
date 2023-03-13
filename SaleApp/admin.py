import pdb
from datetime import datetime, timedelta

from flask_admin import Admin, BaseView, expose
import flask_login as login
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from SaleApp.init import db, app
from SaleApp import utils
from SaleApp.models import Category, Product, User, UserRole, ReceiptDetails, Receipt
from SaleApp import *
from SaleApp import utils
from SaleApp.init import app, db
from SaleApp.models import Category, Product, User, UserRole, ReceiptDetails, Receipt
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user, logout_user
from flask import redirect, render_template, request

app.secret_key = '#@!$%^#$^$#!@%$@#$^%*&^%dsad!2321321r%^%$&^%Sfdfds'


# class AuthenticatedModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.admin)
#
#
# class AuthenticatedView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class ListProductView(ModelView):
    can_view_details = True
    can_export = True
    can_edit = True
    column_display_pk = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'create_date']
    column_sortable_list = ['name', 'price']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin


class ListAccount(ModelView):
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class AccountSignupView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def account_signup(self):
        err_msg = ''
        if request.method.__eq__('POST'):
            user_role = request.form.get('userrole')
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            try:
                if password.strip().__eq__(confirm_password.strip()):
                    err_msg = 'Tạo tài khoản thành công !'
                    utils.account_signup(name=name,
                                         username=username,
                                         password=password,
                                         user_role=user_role)
                    return self.render('admin/signup.html', succes_msg=err_msg)
                else:
                    err_msg = 'Mật khẩu không khớp'

            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        return self.render('admin/signup.html', err_msg=err_msg)


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = utils.count_product_by_cate()
        return self.render('/admin/index.html', stats=stats)

    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.user_role == 'admin'


class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = utils.stats_revenue_by_prod(kw=request.args.get('kw'),
                                            from_date=request.args.get('from_date'),
                                            to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin


class ReceiptView(ModelView):
    @expose('/')
    def index(self):
        receipts = utils.load_receipts()
        return self.render('admin/receipts.html', receipts=receipts)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin


class CategoryView(ModelView):
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin


admin = Admin(app=app, template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(CategoryView(Category, db.session, name='Loại sản phẩm'))
admin.add_view(ListProductView(Product, db.session, name='Quản lý sản phẩm'))
admin.add_view(ReceiptView(Receipt, db.session, name='Hóa đơn'))
admin.add_view(ListAccount(User, db.session, name="Quản lý tài khoản"))
admin.add_view(AccountSignupView(name='Đăng ký tài khoản', endpoint='signup'))
admin.add_view(LogoutView(name='Đăng xuất'))
