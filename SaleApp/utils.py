import pdb
from datetime import datetime

from flask_login import current_user
from sqlalchemy import func

from oucomputer.SaleApp.init import db, app
from oucomputer.SaleApp.models import User, UserRole, Category, Product, Receipt, ReceiptDetails, Comment, Rule
import hashlib


def add_user(name, username, phone, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(),
                username=username.strip(),
                phone=phone.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Product.id).order_by(-Product.id).all()


# def stats_user_register():
#     return User.query.filter(User.joined_date).group_by(User.joined_date)


def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id)) \
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True) \
        .group_by(Category.id).all()


def check_user_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_categories():
    query = Category.query

    return query.all()


def load_products(category_id=None, keyword=None):  # lay tat ca cac sach
    query = Product.query

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))

    elif keyword:
        query = query.filter(Product.name.contains(keyword))
    return query.order_by(Product.created_date.desc()).all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_rule_by_id(rule_id):
    return Rule.query.get(rule_id)


def load_receipts():
    return Receipt.query.all()


def get_receipt_by_id(receipt_id):
    return Receipt.query.get(receipt_id)


def cart_stats(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }


def save_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

            product = get_product_by_id(c['id'])
            product.quantity -= c['quantity']

        db.session.commit()


def save_product(name, price, quantity, description, image):
    product = Product(name=name, price=price, quantity=quantity, description=description, image=image)

    db.session.add(product)
    db.session.commit()


def load_comments(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).all()


def save_comment(content, product_id):
    cmt = Comment(content=content, product_id=product_id, user=current_user)
    db.session.add(cmt)
    db.session.commit()
    return cmt
