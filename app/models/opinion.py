class Opinion():
    def __init__(self, opinion):
        self.selectors = {
        "author": ["span.user-post__author-name"],
        "recommendation": ["span.user-post__author-recomendation > em"],
        "stars": ["span.user-post__score-count"],
        "content": ["div.user-post__text"],
        "useful": ["button.vote-yes > span"],
        "useless": ["button.vote-no > span"],
        "published": ["span.user-post__published > time:nth-child(1)", "datetime"],
        "purchased": ["span.user-post__published > time:nth-child(2)", "datetime"],
        "pros": ["div[class$=positives] ~ div.review-feature__item", None, True],
        "cons": ["div[class$=negatives] ~ div.review-feature__item", None, True]
        }

        self.single_opinion = {
                    key:Opinion.get_item(opinion, *value)
                        for key, value in self.selectors.items()
                }
        self.single_opinion["opinion_id"] = opinion["data-entry-id"]
        
    def get_item(ancestor, selector, attribute=None, return_list=False):
        try:
            if return_list:
                return [item.get_text().strip() for item in ancestor.select(selector)]
            if attribute:
                return ancestor.select_one(selector)[attribute]
            return ancestor.select_one(selector).get_text().strip()
        except (AttributeError, TypeError):
            return None

    