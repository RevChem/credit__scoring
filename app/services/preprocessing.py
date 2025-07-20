import pandas as pd
import logging
import logging.config
import yaml
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler


with open('../config/logging_config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger('services')


def merge_datasets(*dfs):
    return pd.merge(*dfs, on='UID', how='inner')


def uniq_categorical(df, column):
    unique_purposes = df[column].unique()
    standardized = {}
    threshold = 80  

    for purpose in unique_purposes:
        match = process.extractOne(purpose, list(standardized.keys()), scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            standardized[purpose] = standardized[match[0]]
        else:
            standardized[purpose] = purpose

    df[column] = df[column].map(standardized) 
    return df


def quantile95(df):
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        upper = df[col].quantile(0.95)
        df = df[df[col] <= upper]
    return df


def categorical_processing(df1, df2):

    logger.info("Starting data preprocessing")
    df = merge_datasets(df1, df2)
    df.drop(['UID', 'ALL_TimeSinceMostRecentDefault', 'ALL_AgeOfOldestAccount',
             'ApplicationDate', 'ALL_Count', 'ALL_CountDefaultAccounts'], axis=1, inplace=True)
    
    df['LoanPurpose'] = df['LoanPurpose'].str.lower()
    df=uniq_categorical(df, 'LoanPurpose')

    # Из-за этой части возникает необходимость в переобучении
    value_counts = df['LoanPurpose'].value_counts()
    common = value_counts[value_counts >= 15].index
    df['LoanPurpose'] = df['LoanPurpose'].apply(lambda x: x if x in common else 'other')

    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    num_cols = df.select_dtypes(include=['int64', 'float64']).drop('Success', axis=1).columns.tolist()

    df = pd.get_dummies(df, columns=cat_cols, drop_first=True).astype(int)
    logger.info(f"num cols: {df.shape}")

    X = df.drop('Success', axis=1)
    y = df['Success']

    scaler = RobustScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y)

    return X_train, X_test, y_train, y_test