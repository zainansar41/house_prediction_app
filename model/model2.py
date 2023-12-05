import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load the dataset
data = pd.read_csv('C:\\Users\\Hp\\Desktop\\zameen-property-data.csv')
data = data.drop(columns=['Unnamed: 4', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'])

data_new = data.dropna()

location_status = data_new.groupby('location')['location'].agg('count').sort_values(ascending=True)

location_less_than_50 = location_status[location_status < 100]

data_new = data_new[~data_new['location'].isin(location_less_than_50.index)]
data_new = data_new[data_new['bedrooms'] != 0]

data_new['location'] = np.where(data_new['location'].isin(location_less_than_50.index), 'Others', data_new['location'])

data_new['location'] = data_new['location'].str.lower()

dummies = pd.get_dummies(data_new['location'])
new_data = pd.concat([data_new, dummies], axis='columns')

new_data1 = new_data[new_data.baths < new_data.bedrooms + 2]

min_area = new_data1['area'].quantile(0.01)
max_area = new_data1['area'].quantile(0.99)

filtered_data = new_data1[(new_data1['area'] >= min_area) & (new_data1['area'] <= max_area)]


def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = np.mean(subdf.area)
        st = np.std(subdf.area)
        reduced_df = subdf[(subdf.area > (m - st)) & (subdf.area <= (m + st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
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
            stats = bedrooms_stats.get(bedrooms - 1)
            if stats and stats['count'] > 5:
                exclude_indices = np.append(exclude_indices, bedrooms_df[bedrooms_df.area < (stats['mean'])].index.values)
    return df.drop(exclude_indices, axis='index')


filtered_data = remove_pps_outliers(filtered_data)
filtered_data = remove_bedrooms_outliers(filtered_data)
filtered_data = filtered_data.drop(['location'], axis='columns')
filtered_data = filtered_data.drop(['baths'], axis='columns')
filtered_data = filtered_data[filtered_data.purpose != 0]
filtered_data = filtered_data.drop(['purpose'], axis='columns')

X = filtered_data.drop(['price'], axis='columns')
y = filtered_data['price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build a 4-layered ANN model
model_ann = Sequential()
model_ann.add(Dense(128, input_dim=X_train_scaled.shape[1], activation='relu'))
model_ann.add(Dense(64, activation='relu'))
model_ann.add(Dense(32, activation='relu'))
model_ann.add(Dense(1, activation='linear'))  # Output layer with linear activation for regression

# Compile the model
model_ann.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train the ANN model
model_ann.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))

# Evaluate the model on the test set
mse, mae = model_ann.evaluate(X_test_scaled, y_test)
print(f'Mean Squared Error: {mse}, Mean Absolute Error: {mae}')


# Function to predict the price using the ANN model
def predict_price_ann(property_type, City, area, bedrooms, location):
    loc_index = np.where(X.columns == location)[0][0]

    x = np.zeros(len(X.columns))
    x[0] = property_type
    x[1] = City
    x[2] = area
    x[3] = bedrooms
    if loc_index >= 0:
        x[loc_index] = 1

    # Standardize input features before making predictions
    x_scaled = scaler.transform([x])
    return model_ann.predict(x_scaled)[0][0]


# Example usage
predicted_price = predict_price_ann(1, 4, 0.5, 3, 'others')
print(f'Predicted Price: {int(predicted_price)}')
