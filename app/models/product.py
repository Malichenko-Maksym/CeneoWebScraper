class Product():
    def __init__(self, opinions):
        self.opinions = opinions
        self.stats = {
            "opinions_count": len(opinions),
            "pros_count": opinions["pros"].map(bool).sum(),
            "cons_count": opinions["cons"].map(bool).sum(),
            "average_score": opinions["stars"].mean().round(2)
        }