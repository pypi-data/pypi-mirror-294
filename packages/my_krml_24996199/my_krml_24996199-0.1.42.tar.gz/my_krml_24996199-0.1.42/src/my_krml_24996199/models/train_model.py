import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV,RandomizedSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score, roc_curve,confusion_matrix
import matplotlib.pyplot as plt
import joblib
import os
import seaborn as sns


def evaluate_model(model, X_val, y_val, model_name):
    y_pred_prob = model.predict_proba(X_val)[:, 1]
    y_pred_class = model.predict(X_val)
    roc_auc = roc_auc_score(y_val, y_pred_prob)
    accuracy = accuracy_score(y_val, y_pred_class)
    precision = precision_score(y_val, y_pred_class)
    recall = recall_score(y_val, y_pred_class)
    f1 = f1_score(y_val, y_pred_class)
    print(f'{model_name} Performance:')
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1 Score: {f1:.4f}')
    print(f'AUC-ROC: {roc_auc:.4f}')
    fpr, tpr, _ = roc_curve(y_val, y_pred_prob)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', label=f'{model_name} (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='red', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for {model_name}')
    plt.legend()
    plt.show()
    conf_matrix = confusion_matrix(y_val, y_pred_class)
    print("Confusion Matrix:")
    print(conf_matrix)
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Confusion Matrix for {model_name}')
    plt.show()

def train_model(model_name, model, input_filepath, output_model_filepath):
    df = pd.read_csv(input_filepath)
    X = df.drop(columns=['drafted'])
    y = df['drafted']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model.fit(X_train, y_train)
    evaluate_model(model, X_val, y_val, model_name)
    model_dir = os.path.dirname(output_model_filepath)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    joblib.dump(model, output_model_filepath)
    print(f"Model saved to {output_model_filepath}")

def train_model_with_randomsearch(model_name, model, param_grid, input_filepath, output_model_filepath, n_iter=50):
    df = pd.read_csv(input_filepath)
    X = df.drop(columns=['drafted'])
    y = df['drafted']
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Initialize RandomizedSearchCV
    random_search = RandomizedSearchCV(model, param_distributions=param_grid, n_iter=n_iter, 
                                       cv=5, scoring='roc_auc', n_jobs=-1, verbose=1, random_state=42)
    random_search.fit(X_train, y_train)

    # Get the best model
    best_model = random_search.best_estimator_
    evaluate_model(best_model, X_val, y_val, model_name + '_best')
    
    # Save the best model
    best_model_filepath = output_model_filepath.replace('.pkl', '_best_model.pkl')
    joblib.dump(best_model, best_model_filepath)
    print(f"Best model saved to {best_model_filepath}")
    print(f"Best parameters found: {random_search.best_params_}")

if __name__ == '__main__':
    model_name = 'logistic_regression_poly2'
    model = Pipeline([
        ('poly', PolynomialFeatures(degree=2)),
        ('logreg', LogisticRegression(class_weight='balanced', max_iter=1000))
    ])
    input_filepath = '../data/processed/train_processed.csv'
    output_model_filepath = f'../models/{model_name}_model.pkl'
    train_model(model_name, model, input_filepath, output_model_filepath)
