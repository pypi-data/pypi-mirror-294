import pandas as pd
import joblib
import os

def predict_model(input_filepath, model_filepath, output_filepath, selected_features_filepath):
    df = pd.read_csv(input_filepath)
    model = joblib.load(model_filepath)
    if selected_features_filepath is not None:
        selected_features = joblib.load(selected_features_filepath)
        X = df[selected_features]
    else:
        X = df.drop(columns=['drafted', 'player_id'], errors='ignore')
    predictions = model.predict_proba(X)[:, 1]
    submission = pd.DataFrame({
        'player_id': df['player_id'],
        'drafted': predictions
    })
    submission.to_csv(output_filepath, index=False)
    
if __name__ == '__main__':
    model_name = 'logistic_regression_poly2'
    input_filepath = '../data/processed/test_processed.csv'
    model_filepath = f'../models/{model_name}_model.pkl'
    selected_features_filepath = '../models/selected_features.pkl'  # Path to the saved selected features
    output_filepath = f'../models/submission_{model_name}.csv'
    
    predict_model(input_filepath, model_filepath, output_filepath, selected_features_filepath)
