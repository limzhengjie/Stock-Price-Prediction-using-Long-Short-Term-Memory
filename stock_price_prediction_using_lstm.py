# -*- coding: utf-8 -*-
"""Stock Price Prediction using LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JaQtFezrZx_-OWGca2um7xuZaA-iZUEY
"""

import math
import yfinance as yf
import pandas_datareader as ewb
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

df = yf.download("AAPL", start="2006-01-01")
df

df.shape

plt.figure(figsize=(16,8))
plt.title('Close Price History of Apple')
plt.plot(df['Adj Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel ('Close Price USD ($)', fontsize =18)

plt.show()

data = df.filter(['Adj Close'])

dataset = data.values
training_data_len = math.ceil(len(dataset) * .8)

training_data_len

# Scale the daya
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data



# Create the training dataset (index 0 - training data length, and get back all the data)
train_data = scaled_data[0:training_data_len,:]

x_train = []
y_train = []

for i in range(60, len(train_data)):
  # index 0 to 60
  x_train.append(train_data[i-60:i,0])
  # from index 61st
  y_train.append(train_data[i,0])
  if i<=61:
    print(x_train)
    print(y_train)
    print()

x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
x_train.shape

model = Sequential()
model.add(LSTM(50, return_sequences= True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train, y_train, batch_size=1, epochs=1)

# Create the testing dataset
# Create a new array containing scaled values from index 3410 to 3470
test_data = scaled_data[training_data_len - 60:, :]

x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i,0])

x_test = np.array(x_test)
x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1], 1))
x_test.shape

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Get the root mean squared error (RMSE) = accuracy
rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
rmse

# Plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize = (16,8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Adj Close'])
plt.plot(valid[['Adj Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')

plt.show()

# Show the real prices and the predicted prices

valid

apple_quote = yf.download("AAPL")