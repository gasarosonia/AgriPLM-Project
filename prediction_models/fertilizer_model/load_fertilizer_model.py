import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Now we need to define the function that will be called to make predictions

def predict_fertilizer(Nitrogen,Phosphorus,Potassium,ph,Rainfall,Temperature,predicted_crop):
    # The Crop categories will be used in OneHotEncoder to meet the required model feed in features
    df = pd.DataFrame({
        'Nitrogen':Nitrogen,
        'Phosphorus':Phosphorus,
        'Potassium':Potassium,
        'pH':ph,
        'Rainfall':Rainfall,
        'Temperature':Temperature,
        },
        index=[0])
    
    df1 = pd.DataFrame({
        'Crop': ['Sugarcane', 'Maize', 'Groundnut', 'Rice', 'Wheat', 'Soybean']
    })
  
    # We are going to pre-fit OneHotEncoder with these categorical features
    encoder = OneHotEncoder(sparse_output=False,drop='first')
    ct1 = ColumnTransformer(transformers=
                           [('enc',encoder,[0])],
                           verbose_feature_names_out=False)
    ct1.set_output(transform='pandas')
    ct1.fit_transform(df1)
    # Here we call OneHotEncoder to transform new inserted crop feature
    crop_feature = ct1.transform([[predicted_crop]])

    # Concatenate the continuous features and transformed crop feature
    pred_input = pd.concat([df,crop_feature],axis=1)
    
    # load model
    model = pickle.load(open("./prediction_models/fertilizer_model/fertilizer_recommendation_model.pkl", "rb"))
    
    # make predictions
    prediction = model.predict(pred_input).tolist()[0]
    
    return prediction