import matplotlib
matplotlib.use ('pdf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("Boston.csv")
print (dataset.head())

# dataset.shape gives us 506 observartios
# independent and dependent variables
X = dataset.drop(['Unnamed: 0', 'medv'], axis=1)
y = dataset['medv']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

from sklearn.linear_model import LinearRegression

regressor = LinearRegression() # instantiating a object
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)# y_test)

from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_test, y_pred) # measure how far off from the real values

plt.scatter(y_test, y_pred)
plt.xlabel("Prices: $Y_i$")
plt.ylabel("Predicted prices: $\hat{Y}_i$")
plt.title("Prices vs Predicted prices: $Y_i$ vs $\hat{Y}_i$")

plt.savefig('/tmp/outfig', bbox_inches='tight')


