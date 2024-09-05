import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
import numpy as np
import joblib
from sklearn.cluster import KMeans
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings("ignore")
def build_features(input_filepath, output_filepath, is_train=True, selected_features_path=None):
    df = pd.read_csv(input_filepath, low_memory=False, encoding='utf-8')
    print('data loaded')
    if 'Rec_Rank' in df.columns:
        df['Rec_Rank'].fillna(df['Rec_Rank'].mode()[0], inplace=True)

    if 'num' in df.columns:
        df['num'].fillna(df['num'].mode()[0], inplace=True)

    if 'dunks_ratio' in df.columns:
        df['dunks_ratio'].fillna(df['dunks_ratio'].median(), inplace=True)

    if 'pick' in df.columns:
        df['pick'].fillna(df['pick'].mode()[0], inplace=True)

    if 'drtg' in df.columns:
        df['drtg'].fillna(df['drtg'].median(), inplace=True)

    if 'adrtg' in df.columns:
        df['adrtg'].fillna(df['adrtg'].median(), inplace=True)

    if 'dporpag' in df.columns:
        df['dporpag'].fillna(df['dporpag'].median(), inplace=True)

    if 'stops' in df.columns:
        df['stops'].fillna(df['stops'].median(), inplace=True)

    if 'bpm' in df.columns:
        df['bpm'].fillna(df['bpm'].median(), inplace=True)

    if 'obpm' in df.columns:
        df['obpm'].fillna(df['obpm'].median(), inplace=True)

    if 'dbpm' in df.columns:
        df['dbpm'].fillna(df['dbpm'].median(), inplace=True)

    if 'gbpm' in df.columns:
        df['gbpm'].fillna(df['gbpm'].median(), inplace=True)

    if 'mp' in df.columns:
        df['mp'].fillna(df['mp'].median(), inplace=True)

    if 'ogbpm' in df.columns:
        df['ogbpm'].fillna(df['ogbpm'].median(), inplace=True)

    if 'dgbpm' in df.columns:
        df['dgbpm'].fillna(df['dgbpm'].median(), inplace=True)

    if 'oreb' in df.columns:
        df['oreb'].fillna(df['oreb'].median(), inplace=True)

    if 'dreb' in df.columns:
        df['dreb'].fillna(df['dreb'].median(), inplace=True)

    if 'treb' in df.columns:
        df['treb'].fillna(df['treb'].median(), inplace=True)

    if 'ast' in df.columns:
        df['ast'].fillna(df['ast'].median(), inplace=True)

    if 'stl' in df.columns:
        df['stl'].fillna(df['stl'].median(), inplace=True)

    if 'blk' in df.columns:
        df['blk'].fillna(df['blk'].median(), inplace=True)

    if 'pts' in df.columns:
        df['pts'].fillna(df['pts'].median(), inplace=True)
    if 'midmade_midmiss' in df.columns:
        df['midmade_midmiss'].fillna(df['midmade_midmiss'].median(), inplace=True)
    if 'yr' in df.columns:
        df = df[~df['yr'].isin(['0', '57.1', '42.9'])]
        df['yr'].fillna(df['yr'].mode()[0], inplace=True)
        df['yr'] = df['yr'].astype(str)
    if 'mid_ratio' in df.columns:
        df['mid_ratio'].fillna(df['mid_ratio'].median(), inplace=True)
    if 'dunksmiss_dunksmade' in df.columns:
        df['dunksmiss_dunksmade'].fillna(df['dunksmiss_dunksmade'].median(), inplace=True)
    if 'dunksmade' in df.columns:
        df['dunksmade'].fillna(df['dunksmade'].median(), inplace=True)
    if 'midmade' in df.columns:
         df['midmade'].fillna(df['midmade'].median(), inplace=True)
    if 'rimmade_rimmiss' in df.columns:
        df['rimmade_rimmiss'].fillna(df['rimmade_rimmiss'].median(), inplace=True)
    if 'rim_ratio' in df.columns:
        df['rim_ratio'].fillna(df['rim_ratio'].median(), inplace=True)
    if 'ast_tov' in df.columns:    
        df['ast_tov'].fillna(df['ast_tov'].median(), inplace=True)
    if 'rimmade' in df.columns:
        df['rimmade'].fillna(df['rimmade'].median(), inplace=True)
    
    df = df.drop(columns=['ht','num','pick'],axis = 1)      
    duplicate_rows = df.duplicated()
    if duplicate_rows.any():
        print(f"Found {duplicate_rows.sum()} duplicate rows.")
        df = df.drop_duplicates()
        print(f"Duplicates removed. Data now has {len(df)} rows.")

    def outliers_handling(df, column, lower_quantile=0.05, upper_quantile=0.95):
        lower = df[column].quantile(lower_quantile)
        upper = df[column].quantile(upper_quantile)

        def iqr_value(x):
            if x < lower:
                return lower
            elif x > upper:
                return upper
            else:
                return x

        df[column] = df[column].apply(iqr_value)
        return df
    if 'adjoe' in df.columns:
        df = outliers_handling(df, 'adjoe')    
    if 'pfr' in df.columns:
        df = outliers_handling(df, 'pfr')    
    if 'drtg' in df.columns:
        df = outliers_handling(df, 'drtg')
    if 'adrtg' in df.columns:
        df = outliers_handling(df, 'adrtg')
    
    if not is_train and 'player_id' in df.columns:
        player_id = df['player_id']
    else:
        player_id = None

    if is_train:
        features = df.columns.drop('drafted')
    else:
        features = df.columns.drop('player_id') if 'player_id' in df.columns else df.columns

    if is_train:
        y = df['drafted']
        X = df[features]
    else:
        X = df[features]
    
    numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns
    print("Numerical Features",numeric_features)
    print("Categorical Features",categorical_features)

    for col in categorical_features:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    X_processed_numeric = numeric_transformer.fit_transform(X[numeric_features])

    X_processed = np.hstack((X_processed_numeric, X[categorical_features].values))

    if is_train:
        rf = RandomForestClassifier(n_estimators=200, random_state=42)
        rf.fit(X_processed, y)

        selector = SelectFromModel(rf, threshold="median", prefit=True)
        X_selected = selector.transform(X_processed)

        selected_feature_names = np.array(list(numeric_features) + list(categorical_features))[selector.get_support()]
        
        joblib.dump(selected_feature_names, selected_features_path)
        # if 'yr' not in selected_feature_names:
            # selected_feature_names = np.append(selected_feature_names, 'yr')
            # X_selected = np.hstack((X_selected, X[['yr']].values))
        print("Selected Features",selected_feature_names)
        df_processed = pd.DataFrame(X_selected, columns=selected_feature_names)
        df_processed['drafted'] = y.values
    else:
        selected_feature_names = joblib.load(selected_features_path)
        X_selected = X_processed[:, np.isin(np.array(list(numeric_features) + list(categorical_features)), selected_feature_names)]
        df_processed = pd.DataFrame(X_selected, columns=selected_feature_names)

    if player_id is not None:
        df_processed['player_id'] = player_id.values

    df_processed.to_csv(output_filepath, index=False)


def kmeans_imputer(df, n_clusters=8, max_iter=300):
    # Only apply KMeans on numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    kmeans = KMeans(n_clusters=n_clusters, max_iter=max_iter, random_state=42)
    print("Running K mewans Imputer")
    # Create a copy of the DataFrame to work on
    filled_df = df.copy()
    
    # Fit KMeans on non-missing values for each numeric column
    for col in numeric_cols:
        if filled_df[col].isnull().sum() > 0:
            # Fit KMeans on non-missing values
            non_missing_values = filled_df.loc[~filled_df[col].isnull(), numeric_cols].dropna()
            kmeans.fit(non_missing_values)
            
            # Predict cluster for all rows, using zeros for NaN values temporarily
            clusters = kmeans.predict(filled_df[numeric_cols].fillna(0))
            
            # For missing values, replace with the corresponding cluster's centroid value for that column
            for cluster in range(n_clusters):
                centroid_value = kmeans.cluster_centers_[cluster, numeric_cols.get_loc(col)]
                mask = (clusters == cluster) & (filled_df[col].isnull())
                filled_df.loc[mask, col] = centroid_value
                
    return filled_df

def build_features_k_means(input_filepath, output_filepath, is_train=True, selected_features_path=None):
    df = pd.read_csv(input_filepath, low_memory=False, encoding='utf-8')
    print('data loaded')

    # if 'midmade_midmiss' in df.columns:
    #     df['midmade_midmiss'].fillna(df['midmade_midmiss'].median(), inplace=True)
    if 'yr' in df.columns:
        df = df[~df['yr'].isin(['0', '57.1', '42.9'])]
        df['yr'].fillna(df['yr'].mode()[0], inplace=True)
        df['yr'] = df['yr'].astype(str)
    # Apply KMeans imputation
    df = kmeans_imputer(df)
    # if 'mid_ratio' in df.columns:
    #     df['mid_ratio'].fillna(df['mid_ratio'].median(), inplace=True)
    # if 'dunksmiss_dunksmade' in df.columns:
    #     df['dunksmiss_dunksmade'].fillna(df['dunksmiss_dunksmade'].median(), inplace=True)
    # if 'dunksmade' in df.columns:
    #     df['dunksmade'].fillna(df['dunksmade'].median(), inplace=True)
    # if 'midmade' in df.columns:
    #      df['midmade'].fillna(df['midmade'].median(), inplace=True)
    # if 'rimmade_rimmiss' in df.columns:
    #     df['rimmade_rimmiss'].fillna(df['rimmade_rimmiss'].median(), inplace=True)
    # if 'rim_ratio' in df.columns:
    #     df['rim_ratio'].fillna(df['rim_ratio'].median(), inplace=True)
    # if 'ast_tov' in df.columns:    
    #     df['ast_tov'].fillna(df['ast_tov'].median(), inplace=True)
    # if 'rimmade' in df.columns:
    #     df['rimmade'].fillna(df['rimmade'].median(), inplace=True)
    df = df.drop(columns=['ht','num','pick'],axis = 1)      
    duplicate_rows = df.duplicated()
    if duplicate_rows.any():
        print(f"Found {duplicate_rows.sum()} duplicate rows.")
        df = df.drop_duplicates()
        print(f"Duplicates removed. Data now has {len(df)} rows.")

    def outliers_handling(df, column, lower_quantile=0.05, upper_quantile=0.95):
        lower = df[column].quantile(lower_quantile)
        upper = df[column].quantile(upper_quantile)

        def iqr_value(x):
            if x < lower:
                return lower
            elif x > upper:
                return upper
            else:
                return x

        df[column] = df[column].apply(iqr_value)
        return df
    # if 'adjoe' in df.columns:
    #     df = outliers_handling(df, 'adjoe')    
    if 'pfr' in df.columns:
        df = outliers_handling(df, 'pfr')    
    if 'drtg' in df.columns:
        df = outliers_handling(df, 'drtg')
    if 'adrtg' in df.columns:
        df = outliers_handling(df, 'adrtg')
    
    if not is_train and 'player_id' in df.columns:
        player_id = df['player_id']
    else:
        player_id = None

    if is_train:
        features = df.columns.drop('drafted')
    else:
        features = df.columns.drop('player_id') if 'player_id' in df.columns else df.columns

    if is_train:
        y = df['drafted']
        X = df[features]
    else:
        X = df[features]
    
    numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns
    print("Numerical Features",numeric_features)
    print("Categorical Features",categorical_features)

    for col in categorical_features:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    X_processed_numeric = numeric_transformer.fit_transform(X[numeric_features])

    X_processed = np.hstack((X_processed_numeric, X[categorical_features].values))

    if is_train:
        rf = RandomForestClassifier(n_estimators=200, random_state=42)
        rf.fit(X_processed, y)

        selector = SelectFromModel(rf, threshold="mean", prefit=True)
        X_selected = selector.transform(X_processed)

        selected_feature_names = np.array(list(numeric_features) + list(categorical_features))[selector.get_support()]
        
        joblib.dump(selected_feature_names, selected_features_path)
        if 'yr' not in selected_feature_names:
            selected_feature_names = np.append(selected_feature_names, 'yr')
            X_selected = np.hstack((X_selected, X[['yr']].values))
        print("Selected Features",selected_feature_names)
        df_processed = pd.DataFrame(X_selected, columns=selected_feature_names)
        df_processed['drafted'] = y.values
    else:
        selected_feature_names = joblib.load(selected_features_path)
        X_selected = X_processed[:, np.isin(np.array(list(numeric_features) + list(categorical_features)), selected_feature_names)]
        df_processed = pd.DataFrame(X_selected, columns=selected_feature_names)

    if player_id is not None:
        df_processed['player_id'] = player_id.values

    df_processed.to_csv(output_filepath, index=False)

def build_features_with_smote(input_filepath, output_filepath, is_train=True, selected_features_path=None):
    df = pd.read_csv(input_filepath, low_memory=False, encoding='utf-8')
    print('data loaded')
    if 'Rec_Rank' in df.columns:
        df['Rec_Rank'].fillna(df['Rec_Rank'].mode()[0], inplace=True)

    if 'num' in df.columns:
        df['num'].fillna(df['num'].mode()[0], inplace=True)

    if 'dunks_ratio' in df.columns:
        df['dunks_ratio'].fillna(df['dunks_ratio'].median(), inplace=True)

    if 'pick' in df.columns:
        df['pick'].fillna(df['pick'].mode()[0], inplace=True)

    if 'drtg' in df.columns:
        df['drtg'].fillna(df['drtg'].median(), inplace=True)

    if 'adrtg' in df.columns:
        df['adrtg'].fillna(df['adrtg'].median(), inplace=True)

    if 'dporpag' in df.columns:
        df['dporpag'].fillna(df['dporpag'].median(), inplace=True)

    if 'stops' in df.columns:
        df['stops'].fillna(df['stops'].median(), inplace=True)

    if 'bpm' in df.columns:
        df['bpm'].fillna(df['bpm'].median(), inplace=True)

    if 'obpm' in df.columns:
        df['obpm'].fillna(df['obpm'].median(), inplace=True)

    if 'dbpm' in df.columns:
        df['dbpm'].fillna(df['dbpm'].median(), inplace=True)

    if 'gbpm' in df.columns:
        df['gbpm'].fillna(df['gbpm'].median(), inplace=True)

    if 'mp' in df.columns:
        df['mp'].fillna(df['mp'].median(), inplace=True)

    if 'ogbpm' in df.columns:
        df['ogbpm'].fillna(df['ogbpm'].median(), inplace=True)

    if 'dgbpm' in df.columns:
        df['dgbpm'].fillna(df['dgbpm'].median(), inplace=True)

    if 'oreb' in df.columns:
        df['oreb'].fillna(df['oreb'].median(), inplace=True)

    if 'dreb' in df.columns:
        df['dreb'].fillna(df['dreb'].median(), inplace=True)

    if 'treb' in df.columns:
        df['treb'].fillna(df['treb'].median(), inplace=True)

    if 'ast' in df.columns:
        df['ast'].fillna(df['ast'].median(), inplace=True)

    if 'stl' in df.columns:
        df['stl'].fillna(df['stl'].median(), inplace=True)

    if 'blk' in df.columns:
        df['blk'].fillna(df['blk'].median(), inplace=True)

    if 'pts' in df.columns:
        df['pts'].fillna(df['pts'].median(), inplace=True)
    if 'midmade_midmiss' in df.columns:
        df['midmade_midmiss'].fillna(df['midmade_midmiss'].median(), inplace=True)
    if 'yr' in df.columns:
        df = df[~df['yr'].isin(['0', '57.1', '42.9'])]
        df['yr'].fillna(df['yr'].mode()[0], inplace=True)
        df['yr'] = df['yr'].astype(str)
    if 'mid_ratio' in df.columns:
        df['mid_ratio'].fillna(df['mid_ratio'].median(), inplace=True)
    if 'dunksmiss_dunksmade' in df.columns:
        df['dunksmiss_dunksmade'].fillna(df['dunksmiss_dunksmade'].median(), inplace=True)
    if 'dunksmade' in df.columns:
        df['dunksmade'].fillna(df['dunksmade'].median(), inplace=True)
    if 'midmade' in df.columns:
         df['midmade'].fillna(df['midmade'].median(), inplace=True)
    if 'rimmade_rimmiss' in df.columns:
        df['rimmade_rimmiss'].fillna(df['rimmade_rimmiss'].median(), inplace=True)
    if 'rim_ratio' in df.columns:
        df['rim_ratio'].fillna(df['rim_ratio'].median(), inplace=True)
    if 'ast_tov' in df.columns:    
        df['ast_tov'].fillna(df['ast_tov'].median(), inplace=True)
    if 'rimmade' in df.columns:
        df['rimmade'].fillna(df['rimmade'].median(), inplace=True)
    
    df = df.drop(columns=['ht','num','pick'],axis = 1)      
    duplicate_rows = df.duplicated()
    if duplicate_rows.any():
        print(f"Found {duplicate_rows.sum()} duplicate rows.")
        df = df.drop_duplicates()
        print(f"Duplicates removed. Data now has {len(df)} rows.")

    def outliers_handling(df, column, lower_quantile=0.05, upper_quantile=0.95):
        lower = df[column].quantile(lower_quantile)
        upper = df[column].quantile(upper_quantile)

        def iqr_value(x):
            if x < lower:
                return lower
            elif x > upper:
                return upper
            else:
                return x

        df[column] = df[column].apply(iqr_value)
        return df
    if 'adjoe' in df.columns:
        df = outliers_handling(df, 'adjoe')    
    if 'pfr' in df.columns:
        df = outliers_handling(df, 'pfr')    
    if 'drtg' in df.columns:
        df = outliers_handling(df, 'drtg')
    if 'adrtg' in df.columns:
        df = outliers_handling(df, 'adrtg')
    
    if not is_train and 'player_id' in df.columns:
        player_id = df['player_id']
    else:
        player_id = None

    if is_train:
        features = df.columns.drop('drafted')
    else:
        features = df.columns.drop('player_id') if 'player_id' in df.columns else df.columns

    if is_train:
        y = df['drafted']
        X = df[features]
    else:
        X = df[features]
    
    numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns
    print("Numerical Features",numeric_features)
    print("Categorical Features",categorical_features)

    for col in categorical_features:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    X_processed_numeric = numeric_transformer.fit_transform(X[numeric_features])

    X_processed = np.hstack((X_processed_numeric, X[categorical_features].values))
    # Applying SMOTE if needed and is_train
    if is_train:
        smote = SMOTE(random_state=42)
        X_processed, y = smote.fit_resample(X_processed, y)
        print(f"Applied SMOTE. New class distribution: {pd.Series(y).value_counts()}")

    if is_train:
        rf = RandomForestClassifier(n_estimators=200, random_state=42)
        rf.fit(X_processed, y)

        selector = SelectFromModel(rf, threshold="median", prefit=True)
        X_selected = selector.transform(X_processed)

        selected_feature_names = np.array(list(numeric_features) + list(categorical_features))[selector.get_support()]
        
        joblib.dump(selected_feature_names, selected_features_path)
        # if 'yr' not in selected_feature_names:
            # selected_feature_names = np.append(selected_feature_names, 'yr')
            # X_selected = np.hstack((X_selected, X[['yr']].values))
        print("Selected Features",selected_feature_names)
        df_processed = pd.DataFrame(X_selected, columns=selected_feature_names)
        df_processed['drafted'] = y.values
    else:
        selected_feature_names = joblib.load(selected_features_path)
        X_selected = X_processed[:, np.isin(np.array(list(numeric_features) + list(categorical_features)), selected_feature_names)]
        df_processed = pd.DataFrame(X_selected, columns=selected_feature_names)

    if player_id is not None:
        df_processed['player_id'] = player_id.values

    df_processed.to_csv(output_filepath, index=False)


if __name__ == '__main__':
    print("Preprocessing the training data...")
    build_features('../data/raw/train.csv', '../data/processed/train_processed.csv', is_train=True, selected_features_path='../models/selected_features.pkl')

    print("Preprocessing the test data...")
    build_features('../data/raw/test.csv', '../data/processed/test_processed.csv', is_train=False, selected_features_path='../models/selected_features.pkl')
