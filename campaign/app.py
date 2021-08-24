import pickle
from flask import Flask, render_template, request
import pickle
from os import getenv
import pandas as pd


def create_app():
    APP = Flask(__name__)
    
    categories = ['film & video', 'music', 'technology', 'publishing', 
        'art', 'food', 'games', 'fashion', 'comics', 'design', 'photography',
        'crafts', 'theater', 'journalism', 'dance']
    subcategories = ["web", 'product design', 'accessories', 'tabletop games',
                'photobooks', 'comic books', 'comedy', 'illustration',
                'gadgets', "children's books", 'shorts', 'apparel', 'drinks',
                'graphic novels', 'documentary', 'small batch', 'fiction',
                'restaurants', 'country & folk', 'hardware']
    @APP.route("/")
    def root():
        # data = {'id': [9999999999],
        #     'category':['comics'],
        #     'goal':[2500.0],
        #     'blurb_length':[25],
        #     'campaign_duration':[60],
        #     'sub_category': ['graphic novels']}
        # df = pd.DataFrame(data)
        # df.set_index('id', drop=True, inplace=True)
        # # return render_template('test.html', test_string=df.columns)
        # prediciton = predictor.predict(df)
        # ret_string = ""
        # if prediciton == 1:
        #     ret_string = "this campaign is likely to succeed"
        # else:
        #     ret_string = "this campaign is likely to fail"
        return render_template('home.html', title='Home', categories=categories, subcategories=subcategories)


    @APP.route("/predict", methods=['POST'])
    def predict():
        data = {'id': [9999999999],
            'category':[request.values['category']],
            'goal':[request.values['goal']],
            'blurb_length':[request.values['blurb_length']],
            'campaign_duration':[request.values['campaign_duration']],
            'sub_category': [request.values['sub_category']]
        }
        df = pd.DataFrame(data)
        df.set_index('id', drop=True, inplace=True)
        predictor = pickle.load(open('campaign\prelim_model.pickle', 'rb'))
        prediciton = predictor.predict(df)
        if prediciton == 1:
            pred = "this campaign is likely to succeed"
        else:
            pred = "this campaign is likely to fail"
        return render_template('predict.html', pred=pred)

    return APP