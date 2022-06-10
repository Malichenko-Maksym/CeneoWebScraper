from app.models.opinion import Opinion
from bs4 import BeautifulSoup
from app.utils import get_item
import requests
import numpy as np
import os
import pandas as pd
from matplotlib import pyplot as plt
import json

class Product:
    def __init__(self, product_id, opinions=[], product_name="", opinions_count=0, pros_count=0, cons_count=0, average_score=0):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions
        self.opinions_count = opinions_count
        self.pros_count = pros_count
        self.cons_count = cons_count
        self.average_score = average_score
        return self

    def extract_name():
        url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
        response = requests.get(url)
        page = BeautifulSoup(response.text, "html.parser")
        self.product_name = get_item(page, "h1.product-top__product-info__name")
        return self

    def extract_opinions(self, product_id):
        url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
        while(url):
            response = requests.get(url)
            page = BeautifulSoup(response.text, "html.parser")
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                single_opinion = Opinion().extract_opinion(opinion)
                single_opinion["opinion_id"] = opinion["data-entry-id"]
                self.opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl"+get_item(page,"a.pagination__next","href")
            except TypeError:
                url = None
        return self
    def calculate_stats(self):

        opinions = pd.read_json(json.dumps([opinion.to_dict() for  opinion in self.opinions]))
        opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))

        self.opinions_count = len(opinions)
        self.pros_count = opinions["pros"].map(bool).sum()
        self.cons_coun = opinions["cons"].map(bool).sum()
        self.average_score = opinions["stars"].mean().round(2)
        return self

    def opinions_to_df(self):
        return self


    def draw_charts(self):
        if not os.path.exists("app/plots"):
            os.makedirs("app/plots")
        recommendation = opinions["recommendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam", "Polecam", None], fill_value=0)
        recommendation.plot.pie(
            label="",
            autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',
            colors = ["crimson", "forestgreen", "lightskyblue"],
            labels = ["Nie polecam", "Polecam", "Nie mam zdania"]
        )
        plt.title("Rekomendacje")
        plt.savefig(f"app/plots/{product_id}_recommendations.png")
        plt.close()
        stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        stars.plot.bar(
            color = "pink"
        )
        plt.title("Oceny produktu")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.grid(True, axis="y")
        plt.xticks(rotation=0)
        plt.savefig(f"app/plots/{product_id}_stars.png")
        plt.close()
    
    def __str__(self):
        pass

    def __repr__(self):
        pass

    def to_dict(self):
        pass
    
    def export_opinions():
        if not os.path.exists("app/opinions"):
            os.makedirs("app/opinions")
        with open(f"app/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump([opinion.to_dict() for opinion in self.opinions], jf, indent=4, ensure_ascii=False)

    def export_product():
        pass