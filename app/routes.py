from app import app
from flask import render_template, redirect, url_for, request, send_file
import json
import os
from app.models.product import Product
import re

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        if  bool(re.search(r'\D', product_id)):
            error = "Indeks może zawierać tylko cyfry"
            return render_template("extract.html.jinja", error=error)
        if len(product_id)<5:
            error = "Indeks musi być dłuższy"
            return render_template("extract.html.jinja", error=error)
        if len(product_id)>20:
            error = "Indeks musi być krótszy"
            return render_template("extract.html.jinja", error=error)
        product = Product(product_id)
        product.extract_name()
        if product.product_name:
            product.extract_opinions().calculate_stats().draw_charts()
            product.export_opinions()
            product.export_product()
        else:
            error = "Ups... coś poszło nie tak"
            return render_template("extract.html.jinja", error=error)
        return redirect(url_for('product', product_id=product_id))
        
    else:
        return render_template("extract.html.jinja")

@app.route('/products')
def products():
    products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    return render_template("products.html.jinja", products=products)

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    product.import_product()
    stats = product.stats_to_dict()
    opinions = product.opinions_to_df()
    stars =  product.get_stars()
    data = [stats["pros_count"], stats["cons_count"], stats["opinions_count"]-stats["pros_count"]-stats["cons_count"]]
    product_name = stats["product_name"]
    return render_template("product.html.jinja", product_id=product_id, product_name=product_name, opinions=opinions, data=data, stars=stars)

@app.route('/download/<product_id>')
def download(product_id):
    path = 'opinions\\'+str(product_id)+'.json'
    return send_file(path, as_attachment=True)
    