import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np


def add_suffix(var_origin, suffix='_x', exclude=['time']):
    if isinstance(var_origin, list) or isinstance(var_origin, pd.Index):
        return [var + suffix if var not in exclude else var for var in var_origin]
    elif isinstance(var_origin, str):
        return var_origin + suffix if var_origin not in exclude else var_origin
    else:
        return "Unsupported data type"

def predict_ts(ts_origin,var_origin, ts_train,var_train, model='GBR'):
    """
    Input:
    ts_origin: pandas DataFrame
    var_origin: variable name (str) e.g., ['hs','tp','Pdir','hs_swell']
    ts_train: pandas DataFrame
    var_train: variable name (str) e.g., ['hs']
    model = 'GBR', 'SVR_RBF', LSTM
    Output:
    ts_pred: pandas DataFrame
    """
    Y_pred = pd.DataFrame(columns=[var_train], index=ts_origin.index)

    # Add extension _x, _y
    ts_origin.columns = add_suffix(ts_origin.columns, suffix='_x') 
    ts_train.columns  = add_suffix(ts_train.columns, suffix='_y') 

    var_origin = add_suffix(var_origin, suffix='_x')  
    var_train =  add_suffix(var_train, suffix='_y')  

    # Merge or join the dataframes based on time
    #ts_origin.set_index('time', inplace=True)
    #ts_train.set_index('time', inplace=True)
    merged_data = pd.merge(ts_origin[var_origin], ts_train[var_train], how='inner', left_on='time', right_on='time')

    # Handling missing values if any
    merged_data = merged_data.dropna()
    # Extracting features and target variables
    X = merged_data[var_origin]
    Y = merged_data[var_train]
    
    # Splitting the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.1)

    # Creating and fitting the linear regression model
    from sklearn.linear_model import LinearRegression
    from sklearn.svm import SVR
    from sklearn.ensemble import GradientBoostingRegressor
    if model == 'LinearRegression':
        model = LinearRegression()
        model.fit(X_train, Y_train)
        Y_pred[:] = model.predict(ts_origin[var_origin].values).reshape(-1, 1)    
    elif model == 'SVR_RBF':    
        model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
        model.fit(X_train, Y_train)
        Y_pred[:] = model.predict(ts_origin[var_origin].values).reshape(-1, 1)    
    elif model == 'SVR_LINEAR':            
        model = SVR(kernel="linear", C=100, gamma="auto")
        model.fit(X_train, Y_train)
        Y_pred[:] = model.predict(ts_origin[var_origin].values).reshape(-1, 1)    
    elif model == 'SVR_POLY':    
        model = SVR(kernel="poly", C=100, gamma="auto", degree=3, epsilon=0.1, coef0=1)
        model.fit(X_train, Y_train)
        Y_pred[:] = model.predict(ts_origin[var_origin].values).reshape(-1, 1)    
    elif model == 'GBR':
        model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
        model.fit(X_train, Y_train)
        Y_pred[:] = model.predict(ts_origin[var_origin].values).reshape(-1, 1)    
    elif model == 'LSTM':
        from keras.models import Sequential
        from keras.layers import LSTM, Dense
        from keras.optimizers import Adam
        optimizer = Adam(learning_rate=0.001)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dense(units=1))
        # Compile the model
        model.compile(optimizer=optimizer, loss='mean_squared_error')
        model.fit(X_train, Y_train, epochs=40, batch_size=32, validation_data=(X_test, Y_test), verbose=1)
        Y_pred[:] = model.predict(ts_origin[var_origin].values).reshape(-1, 1) 

    # remove back extension _x, _y
    ts_origin.columns = [col.replace('_x', '') for col in ts_origin.columns]
    ts_train.columns = [col.replace('_y', '') for col in ts_train.columns]
    
    return Y_pred