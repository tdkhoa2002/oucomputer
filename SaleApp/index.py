from flask import render_template

from SaleApp import *
from SaleApp.init import app


@app.route("/")
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
