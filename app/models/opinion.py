from app.parameters import selectors
from app.utils import get_item
class Opinion():
    def __init__(self, author="", recommendation=None, stars=0, content="", useful=0, useless=0, publish_date=None, purchase_date=None, pros=[], cons=[], opinion_id=""):
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.publish_date = publish_date
        self.purchase_date = purchase_date
        self.pros = pros
        self.cons = cons
        self.opinion_id = opinion_id
        return self
    
    def extract_opinion(self, opinion):
        for key, value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
        self.opinion_id = opinion["data-entry-id"]
        return self
    
    def __str__(self):
        return  f"{self.author},{self.recommendation},{self.stars},{self.content},{self.useful },{self.useless },{self.publish_date},{self.purchase_date },{self.pros },{self.cons},{self.opinion_id}"
        

    def __repr__(self):
        return f'Opinion("{self.author}","{self.recommendation}",{self.stars},"{self.content}",{self.useful },{self.useless },"{self.publish_date}","{self.purchase_date}",{self.pros},{self.cons},"{self.opinion_id}")'


    def to_dict(self):
        return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}