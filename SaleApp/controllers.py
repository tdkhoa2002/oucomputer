import hashlib
import pdb
from datetime import datetime, date, timedelta

from flask_admin import AdminIndexView
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

import cloudinary.uploader
from flask import render_template, request, redirect, url_for, session, jsonify, abort
from flask_login import login_user, logout_user, login_required
from pytz import HOUR
from sqlalchemy.sql.functions import now
from oucomputer.SaleApp import utils
from oucomputer.SaleApp.init import app, db
from oucomputer.SaleApp.decorators import annonymous_user
from oucomputer.SaleApp.models import User, Rule, ReceiptDetails, Receipt


def index():  # Trang chu
    msg = ""
    category_id = request.args.get('category_id')
    keyword = request.args.get('keyword')

    products = utils.load_products(category_id=category_id, keyword=keyword)  # lay sach co keyword nguoi dung vua tim kiem
    # hoac lay tat ca cac sach ra

    if not products:
        msg = "Không tìm thấy sản phẩm!"

    return render_template('index.html',
                           products=products, msg=msg)


def details(product_id):  # chi tiet san pham
    b = utils.get_product_by_id(product_id)  # san pham vua click
    return render_template('details.html', product=b)


def category_products(category_id):  # lay sach theo danh muc
    products = utils.load_products(category_id, keyword=None)
    return render_template('categories.html', products=products)


def create_product():
    return render_template('admin/product/create.html')


def post_product():
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        image_path = None

        image = request.files.get('image')
        if image:
            res = cloudinary.uploader.upload(image)
            image_path = res['secure_url']

        utils.save_product(name=name, price=price, description=description, quantity=quantity,
                        image=image_path)
    return redirect('/admin/products')


def delete_product(product_id):
    product = utils.get_product_by_id(product_id)  # lay cuon sach can xoa ra
    db.session.delete(product)  # xoa
    db.session.commit()
    return redirect('/admin/product/')


def edit_product(product_id):
    product = utils.get_product_by_id(product_id)  # lay sach can chinh sua
    return render_template('admin/product/edit.html', product=product)  # tra ve giao dien chinh sua sach do


def update_product(product_id):
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        author = request.form.get('author')

        product = utils.get_product_by_id(product_id)

        product.name = name
        product.price = price
        product.description = description
        product.author = author

        if request.form.getlist('active'):
            product.active = 1
        else:
            product.active = 0
        db.session.commit()

    return redirect('/admin/product/')


def import_products(product_id):
    if request.method.__eq__('POST'):
        quantity = int(request.form.get('quantity'))

        product = utils.get_product_by_id(product_id)

        rule1 = utils.get_rule_by_id(1)
        rule2 = utils.get_rule_by_id(2)
        min_quantity = int(rule1.value)  # So luong nhap toi thieu: 150
        min_stock = int(rule2.value)  # So luong ton trong kho phai be hon: 300

        if product.quantity < min_stock:  # So luong sach trong kho < 300
            if quantity >= min_quantity:  # So luong sach muon nhap > 150
                product.quantity += quantity
            else:
                abort(406)
        else:
            abort(406)
        db.session.commit()
    return redirect('/admin/product/')


def receipt_details(receipt_id):
    receipt = utils.get_receipt_by_id(receipt_id=receipt_id)
    receipt_details = ReceiptDetails.query.filter(ReceiptDetails.receipt_id.__eq__(receipt.id)).all()
    sum = 0
    for product in receipt_details:
        sum += product.quantity * product.price

    return render_template('admin/receipt/receipt-details.html', receipt_details=receipt_details, sum=sum)


def reload_receipt():
    try:
        rule = utils.get_rule_by_id(3)
        query = Receipt.query.filter(Receipt.created_date < datetime.now() - timedelta(hours=rule.value))
        receipts = query.all()
        for receipt in receipts:
            ReceiptDetails.query.filter(ReceiptDetails.receipt_id.__eq__(receipt.id)).delete()
            db.session.commit()

            db.session.delete(receipt)
            db.session.commit()
    except:
        return abort(404, "Error")
    # return
    return redirect('/admin/receipt/')


def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        avatar_path = None

        if username:  # kiểm tra username có bị trùng hay không ?
            user_by_username = User.query.filter(User.username.__eq__(username.strip())).first()
            if user_by_username:
                err_msg = "Ten tai khoan da co nguoi su dung"
            else:
                try:
                    if password.strip().__eq__(confirm.strip()):
                        avatar = request.files.get('avatar')
                        if avatar:
                            res = cloudinary.uploader.upload(avatar)
                            avatar_path = res['secure_url']

                        utils.add_user(name=name, username=username, phone=phone, password=password, email=email,
                                       avatar=avatar_path)
                        return redirect(url_for('index'))
                    else:
                        err_msg = "Xác nhận mật khẩu không đúng"
                except Exception as ex:
                    err_msg = "Hệ thống đang có lỗi: " + str(ex)

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def user_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_user_login(username=username, password=password)  # kiem tra xem du lieu username vs password
        if user:  # co dung trong database hay khong
            if user.active:  # user.active == 1
                login_user(user=user)
                return redirect(url_for('index'))
            elif not user.active:
                err_msg = "Người dùng đã bị admin chặn"
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng"
    return render_template('login.html', err_msg=err_msg)


def logout_my_user():
    logout_user()
    return redirect('/login')


def cart():
    return render_template('cart.html')


def add_to_cart():
    data = request.json
    id = str(data['id'])

    key = app.config['CART_KEY']  # 'cart'
    cart = session[key] if key in session else {}
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        name = data['name']
        price = data['price']
        image = data['image']
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "image": image,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


# @app.route('/api/cart/<product_id>', methods=['PUT'])
def update_cart(product_id):
    key = app.config['CART_KEY']  # 'cart'
    cart = session.get(key)

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


# @app.route('/api/cart/<product_id>', methods=['DELETE'])  # /api/cart/${product_id}
def delete_cart(product_id):
    key = app.config['CART_KEY']  # 'cart'
    cart = session.get(key)

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart=cart))


# @app.route('/api/products/<product_id>/comments')  # /api/products/<product_id>/comments
def comments(product_id):
    data = []
    for cmt in utils.load_comments(product_id=product_id):
        data.append({
            'id': cmt.id,
            'content': cmt.content,
            'created_date': str(cmt.created_date),
            'user': {
                'name': cmt.user.name,
                'avatar': cmt.user.avatar
            }
        })

    return jsonify(data)


# @app.route('/api/products/<product_id>/comments', methods=['post'])
def add_comment(product_id):
    try:
        c = utils.save_comment(product_id=product_id, content=request.json['content'])

    except:
        return jsonify({'status': 500})

    return jsonify({
        'status': 204,
        'comment': {
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.avatar
            }
        }
    })


# @app.route("/api/pay")
@login_required
def pay():
    key = app.config['CART_KEY']  # 'cart'
    cart = session.get(key)

    try:
        utils.save_receipt(cart)
    except Exception as ex:
        print(str(ex))
        return jsonify({'status': 500})
    else:
        del session[key]

    return jsonify({'status': 200})