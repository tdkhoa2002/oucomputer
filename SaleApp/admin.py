import pdb
from datetime import datetime, timedelta

from flask_admin import Admin, BaseView, expose
import flask_login as login
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from oucomputer.SaleApp.init import db, app
from oucomputer.SaleApp import utils
from oucomputer.SaleApp.models import Category, Product, User, UserRole, ReceiptDetails, Rule, Receipt
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user, logout_user
from flask import redirect, render_template, request


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        stats = utils.count_product_by_cate()
        if current_user.user_role == UserRole.user:
            return redirect('/')
        return self.render('/admin/index.html', stats=stats)


class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = utils.stats_revenue(kw=request.args.get('kw'),
                                    from_date=request.args.get('from_date'),
                                    to_date=request.args.get('to_date'))
        # statsUserRegister = utils.
        return self.render('admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductView(ModelView):

    @expose('/')
    def index(self):
        products = utils.load_products()

        return self.render('admin/product/products.html', products=products)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.admin


class CategoryView(ModelView):
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class UserView(ModelView):
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class RuleView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


class ReceiptView(ModelView):
    @expose('/')
    def index(self):
        receipts = utils.load_receipts()
        return self.render('admin/receipt/receipts.html', receipts=receipts)

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='Nhà sách OU', template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(CategoryView(Category, db.session, name="Danh mục"))
admin.add_view(ProductView(Product, db.session, name="Thực hiện tác vụ sách"))
admin.add_view(StatsView(name="Thống kê"))
admin.add_view(UserView(User, db.session, name="Quản lý người dùng"))
admin.add_view(ReceiptView(Receipt, db.session, name="Các hóa đơn"))
admin.add_view(RuleView(Rule, db.session, name="Quy định"))
admin.add_view(LogoutView(name="Đăng xuất"))