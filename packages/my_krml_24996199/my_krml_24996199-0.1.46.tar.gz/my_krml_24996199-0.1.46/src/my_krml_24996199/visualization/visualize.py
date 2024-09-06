import seaborn as sns
import matplotlib.pyplot as plt

def box_plot_num(df):
    plt.figure(figsize=(20, 20))
    sns.boxplot(data=df.select_dtypes(include=['float64', 'int64']), orient='h')
    plt.title('Boxplots for All Numeric Columns')
    plt.show()

def target_dist(df):
    if 'drafted' in df.columns:
        sns.countplot(x='drafted', data=df)
        plt.title('Distribution of Target Variable')
        plt.show()

def plot_corr(df):
    cols_num = df.select_dtypes(include=['float64', 'int64']).columns
    corr_mat = df[cols_num].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_mat, annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

def corr_col(df,val=0.2):
    cols_num = df.select_dtypes(include=['float64', 'int64']).columns
    corr_mat = df[cols_num].corr()
    target_correlation = corr_mat['drafted'].sort_values(ascending=False)
    relevant_features = target_correlation[abs(target_correlation) > val].index
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[relevant_features].corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Matrix of Selected Relevant Features')
    plt.show()

