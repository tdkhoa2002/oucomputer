from flask import render_template, request

from SaleApp import utils
from SaleApp.init import app


@app.route("/")
def home():
    categories = utils.load_categories()

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
