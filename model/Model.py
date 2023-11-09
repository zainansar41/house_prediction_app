import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


data = pd.read_csv('C:\\Users\\Hp\\Desktop\\zameen-property-data.csv')
data = data.drop(columns=['Unnamed: 4', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'])

data_new = data.dropna()

location_status = data_new.groupby('location')['location'].agg('count').sort_values(ascending=True)

location_less_than_50 = location_status[location_status < 100]


data_new = data_new[~data_new['location'].isin(location_less_than_50.index)]
data_new = data_new[data_new['bedrooms'] != 0]

#if location is less than 50 replace the location with others
data_new['location'] = np.where(data_new['location'].isin(location_less_than_50.index), 'Others', data_new['location'])

dummies = pd.get_dummies(data_new['location'])
new_data = pd.concat([data_new, dummies], axis='columns')


new_data1 = new_data[new_data.baths<new_data.bedrooms+2]



min_area = new_data1['area'].quantile(0.01)  # Adjust as needed
max_area = new_data1['area'].quantile(0.99)  # Adjust as needed

filtered_data = new_data1[(new_data1['area'] >= min_area) & (new_data1['area'] <= max_area)]

def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.area)
        st = np.std(subdf.area)
        reduced_df = subdf[(subdf.area>(m-st)) & (subdf.area<=(m+st))]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out

def remove_bedrooms_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bedrooms_stats = {}
        for bedrooms, bedrooms_df in location_df.groupby('bedrooms'):
            bedrooms_stats[bedrooms] = {
                'mean': np.mean(bedrooms_df.area),
                'std': np.std(bedrooms_df.area),
                'count': bedrooms_df.shape[0]
            }
        for bedrooms, bedrooms_df in location_df.groupby('bedrooms'):
            stats = bedrooms_stats.get(bedrooms-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bedrooms_df[bedrooms_df.area<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis='index')

filtered_data = remove_pps_outliers(filtered_data)
filtered_data = remove_bedrooms_outliers(filtered_data)
filtered_data = filtered_data.drop(['location'], axis='columns')
filtered_data = filtered_data.drop(['baths'], axis='columns')
filtered_data = filtered_data[filtered_data.purpose != 0]
filtered_data = filtered_data.drop(['purpose'], axis='columns')

X = filtered_data.drop(['price'], axis='columns')
y = filtered_data['price']


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=.2)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))



def predict_price(property_type,City,area,bedrooms,location):    
    loc_index = np.where(X.columns==location)[0][0]

    x = np.zeros(len(X.columns))
    x[0] = property_type
    x[1] = City
    x[2] = area
    x[3] = bedrooms
    if loc_index >= 0:
        x[loc_index] = 1

    return model.predict([x])[0]
# print(int(predict_price(1,4,.5,3,'Others')))






import pickle

with open('zameen_price_model.pickle','wb') as f:
    pickle.dump(model,f)

import json
columns = {
    'data_columns' : [col.lower() for col in X.columns]
}
with open("columns.json","w") as f:
    f.write(json.dumps(columns))