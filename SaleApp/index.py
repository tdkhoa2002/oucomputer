<<<<<<< HEAD
from flask import render_template, request

from SaleApp import utils
from SaleApp.init import app


@app.route("/")
def home():
    categories = utils.load_categories()
=======
from flask import render_template, session
from oucomputer.SaleApp import controllers, utils
from oucomputer.SaleApp.init import app, login

app.add_url_rule("/", "index", controllers.index)
app.add_url_rule("/products/<int:product_id>", "product-detail", controllers.details)
# app.add_url_rule("/admin/product/create/", "create-product", controllers.create_product(), methods=['GET'])
# app.add_url_rule("/admin/product/post", "post_product", controllers.post_product(), methods=['POST'])
# app.add_url_rule("/admin/product/delete/<int:product_id>", "delete_product", controllers.delete_product())
# app.add_url_rule("/admin/product/edit/<int:product_id>", "edit_product", controllers.edit_product())
# app.add_url_rule("/admin/product/update/<int:product_id>", "update_product", controllers.update_product(), methods=['GET', 'POST'])
# app.add_url_rule("/admin/product/import_products/<int:product_id>", "import_products", controllers.import_products(),
#                  methods=['GET', 'POST'])
app.add_url_rule('/admin/receipt-details/<int:receipt_id>', "receipt_details", controllers.receipt_details)
app.add_url_rule('/admin/receipts/reload_receipt', "reload_receipt", controllers.reload_receipt)
# app.add_url_rule("/category/<int:category_id>", "categories", controllers.category_products())
app.add_url_rule("/register", 'register-user', controllers.user_register, methods=['GET', 'POST'])
app.add_url_rule("/login", 'user-login', controllers.user_login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule("/cart", "cart", controllers.cart)
app.add_url_rule("/api/cart", "add-cart", controllers.add_to_cart, methods=["POST"])
app.add_url_rule('/api/cart/<product_id>', "update_cart", controllers.update_cart, methods=['PUT'])
app.add_url_rule('/api/cart/<product_id>', "delete-cart", controllers.delete_cart, methods=['DELETE'])
app.add_url_rule('/api/products/<product_id>/comments', "comments", controllers.comments)
app.add_url_rule('/api/products/<product_id>/comments', "add_comment", controllers.add_comment, methods=['post'])
app.add_url_rule("/api/pay", "pay", controllers.pay)


@app.context_processor
def common_response():
    categories = utils.load_categories()
    products = utils.load_products()
    return {
        'categories': categories,
        'products': products,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)
>>>>>>> 464668e7cd10b8350936063cf8500b3d43f38f3b

    return render_template('index.html', Category = categories)

@app.route("/list_product")
def list_product():
    categories = utils.load_categories()
    Category_id = request.args.get("Category_id")
    product = utils.load_products(Category_id)
    return render_template('product_1.html', product=product, Category = categories)

@app.route("/product_detail")
def product_detail():
    categories = utils.load_categories()
    Product_id = request.args.get("product_id")
    product = utils.get_product_by_id(Product_id)
    return render_template('product_2.html', product=product, Category = categories)

if __name__ == '__main__':
    app.run(debug=True)
