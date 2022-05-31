from app import app
from flask import render_template, redirect, url_for
import json
import re
import requests
from bs4 import BeautifulSoup
def get_item(ancestor, selector, attribute=None, return_list=False):
    try:
        if return_list:
            return [ item.get_text().strip() for item in ancestor.select( selector)]

        if attribute:
            return ancestor.select_one(selector)[attribute]

        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError,TypeError):
        return None

selectors = {
            "author": ["span.user-post__author-name"],
            "recommendation": ["span.user-post__author-recomendation > em"],
            "stars": ["span.user-post__score-count"],
            "content": ["div.user-post__text"],
            "useful": ["button.vote-yes > span"],
            "useless": ["button.vote-no > span"],
            "published": ["span.user-post__published > time:nth-child(1)","datetime"],
            "purchased": ["span.user-post__published > time:nth-child(2)","datetime"],
            "pros": ["div[class$=positives] ~ div.review-feature__item", None, True],
            "cons": ["div[class$=negatives] ~ div.review-feature__item", None, True]
        }

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route('/extract/<product_id>')
def extract(product_id):
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    all_opinions = []
    while(url):
        print(url)
        response = requests.get(url)
        page = BeautifulSoup(response.text, "html.parser")
        opinions = page.select("div.js_product-review")
        for opinion in opinions:
            single_opinion = {
                key:get_item(opinion, *value)
                    for key, value in selectors.items()
            }
            single_opinion["opinion_id"] = opinion["data-entry-id"]
            all_opinions.append(single_opinion)
        try:
            url = "https://www.ceneo.pl"+page.select_one("a.pagination__next")["href"]
        except TypeError:
            url = None

    with open(f"app/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
        json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
    return redirect(url_for('product', product_id=product_id))

@app.route('/products')
def products():
    pass

@app.route('/author')
def author():
    return render_template("author.html.jinja")

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html.jinja", product_id=product_id)
