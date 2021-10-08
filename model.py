import numpy as np
import pandas as pd
import joblib
from joblib import load

def prediction_generate(text):

    # loading all the required objects
    ML_model = load("flask_test_model.joblib")
    user_rating_model = load("user_final_rating_model.joblib")
    vectorizer = load("vectorizer.joblib")
    df_main = load("df_main.joblib")

    # exception handling in case of user name input which is not in our system
    try:
        # getting the top 20 recommendations for the input user
        d = user_rating_model.loc[text].sort_values(ascending=False)[0:20]
        mean_sentiment_score_ = []

        # predicting top 5 recommendations
        for product in d.index:
            prod_score = 0
            total_reviews_per_product = float(len(df_main[(df_main.name==product)].index))
            for indx in df_main[(df_main.name==product)].index.tolist():
                try:
                    inp = vectorizer.transform([df_main[indx]]).toarray()
    	            # predicting sentiment probability
                    prob = ML_model.predict_proba(inp)[1]
                    if prob>=0.70699:    #obtained from tuning final sentiment model
                        senti_prediction=1
                    else:
                        senti_prediction=0
                    prod_score+=senti_prediction
                except:
                    pass
            mean_sentiment_score_.append((product,prod_score/ total_reviews_per_product))

        a = [i[0] for i in sorted(mean_sentiment_score_, key = lambda x: x[1], reverse=True)][:5]
        ret = str('Here are the top 5 recommendations for the input user:\n %a'%a)
    except:
        ret = 'Opps..we do not have any recommendations for you as our system works only for the existing users. Try shopping with us first.'

    return ret
