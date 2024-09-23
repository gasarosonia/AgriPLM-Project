import pickle
# This function will be called and used to predict crop yield predictions
def predict_yield(Rainfall,Fertilizer,Temperature,Nitrogen,Phosphorus,Potassium):
    model = pickle.load(open('./prediction_models/yield_model/yield_prediction_model.pkl','rb'))
    pred = model.predict([[Rainfall,Fertilizer,Temperature,Nitrogen,Phosphorus,Potassium]]).tolist()[0]
    return pred