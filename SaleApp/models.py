from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from SaleApp.init import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    admin = 1
    user = 2


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(100), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(100), nullable=False)
    price = Column(Float, default=0)
    quantity = Column(Integer, default=300)
    description = Column(String(255))
    image = Column(String(200))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=True)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    phone = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.user)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=True)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=True)


if __name__ == '__main__':
    with app.app_context():

        # db.create_all()

        c1 = Category(name="Máy tính")
        c2 = Category(name="Phụ kiện")

        db.session.add_all([c1, c2])
        db.session.commit()


        p1 = Product(name='Laptop Apple MacBook Pro 16 M1 Pro 2021', description='10 core-CPU/16GB/512GB/16 core-GPU (MK1E3SA/A)', price=50190000,
                     image='https://cdn.tgdd.vn/Products/Images/44/253636/apple-macbook-pro-16-m1-pro-2021-10-core-cpu-600x600.jpg',
                     category_id=1)
        p2 = Product(name='Laptop Asus Gaming ROG Strix SCAR 18', description='i9 13980HX/64GB/2TB/16GB RTX4090/240Hz/Balo/Chuột/Win11(N6039W)', price=124000000,
                     image='https://cdn.tgdd.vn/Products/Images/44/302473/asus-gaming-rog-strix-scar-18-g834jy-i9-n6039w-thumb-600x600.jpg',
                     category_id=1)
        p3 = Product(name='Laptop HP Envy 16 h0205TX', description='i9 12900H/32GB/512GB/6GB RTX3060/Touch/Win11 (7C0T2PA)', price=64890000,
                     image='https://cdn.tgdd.vn/Products/Images/44/302980/hp-envy-16-h0205tx-i9-7c0t2pa-1.jpg',
                     category_id=1)
        p4 = Product(name='Laptop MSI Creator Z16 A12UET', description='i7 12700H/16GB/1TB SSD/6GB RTX3060/120Hz/Túi/Chuột/Win11 (036VN)', price=60990000,
                     image='https://cdn.tgdd.vn/Products/Images/44/274783/msi-creator-z16-a12uet-i7-036vn-200322-110544-600x600.jpg',
                     category_id=1)
        p5 = Product(name='Pin sạc dự phòng Polymer', description='10.000 mAh AVA PJ JP196', price=70000,
                     image='https://cdn.tgdd.vn/Products/Images/57/217434/pin-sac-du-phong-polymer-10000mah-ava-pj-jp196-den-thumb-1-600x600.jpeg',
                     category_id=2)
        p6 = Product(name='Cáp Micro USB 20cm AVA Speed II', description='Thiết kế nhỏ gọn, chất liệu mềm dẻo dễ quấn gọn, dễ mang theo bên mình.', price=20000,
                      image='https://cdn.tgdd.vn/Products/Images/58/217252/cap-micro-20cm-ava-speed-ii-thumb3-600x600.jpeg',
                      category_id=2)
        p7 = Product(name='Ốp lưng iPhone 11 Pro Nhựa dẻo Noble Nake JM', description='Thiết kế trong suốt đẹp mắt, tôn vinh vẻ ngoài cao cấp của iPhone 11 Pro.', price=10000,
                  image='https://cdn.tgdd.vn/Products/Images/60/212054/op-lung-iphone-11-pro-nhua-deo-noble-nake-jm-nude-1-1-600x600.jpg',
                  category_id=2)
        p8 = Product(name='Miếng dán màn hình iPhone 12 Mini', description='Chống trầy xước tối ưu màn hình điện thoại iPhone 12 mini.', price=10000,
                  image='https://cdn.tgdd.vn/Products/Images/1363/230505/mieng-dan-man-hinh-iphone-12-mini-ava-600x600.jpg',
                  category_id=2)

        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
        db.session.commit()


        password = str(hashlib.md5('123123'.encode('utf-8')).hexdigest())
        u = User(name="Admin",
                 username="admin",
                 phone="0123456789",
                 password=password,
                 email="admin123@gmail.com",
                 user_role=UserRole.admin,
                 avatar="https://res.cloudinary.com/de3yhowd4/image/upload/v1669481858/dxyigbm1fnl2dmokkeh2.jpg")
        db.session.add(u)
        cmt1 = Comment(content='san pham nay dep qua', user_id=1, product_id=1)
        cmt2 = Comment(content='Xung dang de mua', user_id=1, product_id=1)

        db.session.add_all([cmt1, cmt2])
        db.session.commit()

