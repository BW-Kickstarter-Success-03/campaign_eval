from datetime import timedelta
import pickle
from flask import Flask, render_template, request
import pickle
import pandas as pd
from .extra_data import subcategories as subc


def create_app():
    APP = Flask(__name__)
    
    categories = ['film & video', 'music', 'technology', 'publishing', 
        'art', 'food', 'games', 'fashion', 'comics', 'design', 'photography',
        'crafts', 'theater', 'journalism', 'dance']
    @APP.route("/")
    def root():
        return render_template('home.html', title='Welcome')


    @APP.route("/input")
    def input():
        subcategories = subc
        return render_template('input.html', title='Input', categories=categories, subcategories=subcategories)

    
    @APP.route("/about")
    def member():
        return render_template("about.html", title="About Us")


    @APP.route("/model_info")
    def info():
        return render_template("model.html", title="Model Info")


    @APP.route("/predict", methods=['POST'])
    def predict():
        data0 = {'id': [9999999999],
            'Primary Category':[request.values['Primary Category']],
            'Subcategory':[request.values['Subcategory']],
            'Backers Count':[request.values['Backers Count']],
            'Campaign Goal':[request.values['Campaign Goal']],
            'Amount Pledged':[request.values['Amount Pledged']],
            'Staff Pick':[0],
            'Description Length':[request.values['Description Length']],
            'Campaign Length':[request.values['Campaign Length']],
            'Holiday Season':[request.values['Holiday Season']],
            'Campaign Launch Length':[request.values['Campaign Launch Length']]
        }
        data1 = {'id': [9999999999],
            'Primary Category':[request.values['Primary Category']],
            'Subcategory':[request.values['Subcategory']],
            'Backers Count':[request.values['Backers Count']],
            'Campaign Goal':[request.values['Campaign Goal']],
            'Amount Pledged':[request.values['Amount Pledged']],
            'Staff Pick':[1],
            'Description Length':[request.values['Description Length']],
            'Campaign Length':[request.values['Campaign Length']],
            'Holiday Season':[request.values['Holiday Season']],
            'Campaign Launch Length':[request.values['Campaign Launch Length']]
        }
        df0 = pd.DataFrame(data0)
        df0.set_index('id', drop=True, inplace=True)
        df1 = pd.DataFrame(data1)
        df1.set_index('id', drop=True, inplace=True)
        predictor = pickle.load(open('test_forest.pkl', 'rb'))
        prediciton0 = predictor.predict(df0)
        prediciton1 = predictor.predict(df1)
        if prediciton0 == 1 and prediciton1 == 1:
            pred = "this campaign is likely to succeed"
        elif prediciton0 == 1 and prediciton1 == 0:
            pred = "this campaign is more likely to succeed without getting picked by kickstarter staff"
        elif prediciton0 == 0 and prediciton1 == 1:
            pred = """this campaign is more likely to succeed if you get picked by kickstarter staff.<br/>
                <a href='https://www.kickstarter.com/blog/introducing-projects-we-love-badges' target="_blank">
                Click here to find out more</a>"""
        else:
            pred = "this campaign is likely to fail"
        return render_template('predict.html', pred=pred, title='Prediction')

    return APP