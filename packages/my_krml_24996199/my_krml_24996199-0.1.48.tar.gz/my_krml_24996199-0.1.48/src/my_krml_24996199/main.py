import os
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from xgboost import XGBClassifier
import my_krml_24996199
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from my_krml_24996199.features.build_features import build_features
from my_krml_24996199.models.train_model import train_model
from  my_krml_24996199.models.predict_model import predict_model
from my_krml_24996199.models.train_model import train_model_with_randomsearch
# from data.make_dataset import main as make_dataset_main
from lightgbm import LGBMClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
def main():
    base_dir = os.path.dirname(__file__)
    raw_train_data_path = os.path.join(base_dir, '..', '..', 'data', 'raw', 'train.csv')
    raw_test_data_path = os.path.join(base_dir, '..', '..', 'data', 'raw', 'test.csv')
    processed_train_data_path = os.path.join(base_dir, '..', '..', 'data', 'processed', 'train_processed.csv')
    processed_test_data_path = os.path.join(base_dir, '..', '..', 'data', 'processed', 'test_processed.csv')
    selected_features_path = os.path.join(base_dir, '..', '..', 'models', 'selected_features.pkl')
    print("Preprocessing the training data...")
    build_features(raw_train_data_path, processed_train_data_path,is_train=True, selected_features_path=selected_features_path)
    
    print("Preprocessing the test data...")
    build_features(raw_test_data_path, processed_test_data_path,is_train=False, selected_features_path=selected_features_path)
    model_name = 'light_gm_model'
    model_filepath = os.path.join(base_dir, '..', '..', 'models', f'{model_name}_model.pkl') 
    print("Training the model...")
    # model = XGBClassifier( random_state=42, use_label_encoder=False, eval_metric='logloss')
    model = LGBMClassifier( random_state=42)
    param_grid = {
    'boosting_type': ['gbdt'],
    # , 'dart', 'goss'],  
    'num_leaves': [31],
    'max_depth': [-1, 5, 10, 15, 20],
    'learning_rate': [0.001, 0.01, 0.1],
    'n_estimators': [100, 200, 500, 1000],  # Number of boosting iterations
    'min_child_weight': [1, 5, 10],  # Minimum sum of instance weight (hessian) needed in a child
    'subsample': [0.6, 0.7],  # Subsample ratio of the training instances
    # 'subsample_freq': [0, 5, 10],  # Frequency of subsampling
    # 'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],  # Subsample ratio of columns when constructing each tree
    # 'reg_alpha': [0, 0.1, 0.5, 1],  # L1 regularization term on weights
    # 'reg_lambda': [0, 0.1, 0.5, 1],  # L2 regularization term on weights
    # 'min_split_gain': [0.0, 0.1, 0.2],  # Minimum gain to make a split
    'scale_pos_weight': [1, 5, 10, 20]  # Balancing of positive and negative weights
    }
    # base_models = [
    # ('xgb', XGBClassifier(n_estimators=300, random_state=42)),
    # ('lgbm', LGBMClassifier(n_estimators=200, random_state=42)),
    # ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    # ]
    # model = StackingClassifier(estimators=base_models, final_estimator=LGBMClassifier(n_estimators=100, random_state=42))
    # model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
    # model = RandomForestClassifier(n_estimators=400, random_state=42)
    train_model(model_name, model, processed_train_data_path, model_filepath)
    train_model_with_randomsearch(model_name, model, param_grid, processed_train_data_path, model_filepath)
    print("Making predictions with the model...")
    submission_filepath = os.path.join(base_dir, '..', '..', 'models', f'submission_{model_name}.csv')
    predict_model(processed_test_data_path, model_filepath, submission_filepath, selected_features_path)

    print("Pipeline completed successfully!")

if __name__ == '__main__':
    main()