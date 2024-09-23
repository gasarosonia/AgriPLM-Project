import pickle
# This function will be called and used to predict recommended crop to grow
def predict_crop(Nitrogen,Phosphorus,Potassium,pH,Rainfall,Temperature):
    model = pickle.load(open('./prediction_models/crop_model/crop_recommendation_model.pkl', 'rb'))
    pred = model.predict([[Nitrogen,Phosphorus,Potassium,pH,Rainfall,Temperature]]).tolist()[0]
    return pred