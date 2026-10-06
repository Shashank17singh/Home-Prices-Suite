"""
Data cleaning, feature engineering, and model training script for Bengaluru house prices.
"""
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import ShuffleSplit, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def convert_sqft_to_num(x):
    try:
        tokens = str(x).split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        return float(x)
    except:
        return None


def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out


def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk - 1)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(
                    exclude_indices, bhk_df[bhk_df.price_per_sqft < (stats['mean'])].index.values
                )
    return df.drop(exclude_indices, axis='index')


def train_model(data_path: str, model_path: str, columns_path: str):
    df = pd.read_csv(data_path)
    df = df.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')
    df = df.dropna()

    df['bhk'] = df['size'].apply(lambda x: int(str(x).split(' ')[0]))
    df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_num)
    df = df.dropna()

    df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']

    df.location = df.location.apply(lambda x: str(x).strip())
    location_stats = df.groupby('location')['location'].agg('count').sort_values(ascending=False)
    location_stats_less_than_10 = location_stats[location_stats <= 10]
    df.location = df.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

    df = df[~(df.total_sqft / df.bhk < 300)]
    df = remove_pps_outliers(df)
    df = remove_bhk_outliers(df)
    
    df = df[df.bath < df.bhk + 2]
    df = df.drop(['size', 'price_per_sqft'], axis='columns')

    dummies = pd.get_dummies(df.location)
    df = pd.concat([df, dummies.drop('other', axis='columns')], axis='columns')
    df = df.drop('location', axis='columns')

    X = df.drop(['price'], axis='columns')
    y = df.price

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

    lr_clf = make_pipeline(StandardScaler(), LinearRegression())
    lr_clf.fit(X_train, y_train)
    
    print(f"Model trained. Test Score: {lr_clf.score(X_test, y_test):.4f}")

    with open(model_path, 'wb') as f:
        pickle.dump(lr_clf, f)

    columns = {'data_columns': [col.lower() for col in X.columns]}
    with open(columns_path, "w") as f:
        f.write(json.dumps(columns))

if __name__ == "__main__":
    train_model(
        'Bengaluru_House_Data.csv', 
        'banglore_home_prices_model.pickle', 
        'columns.json'
    )