# Classification using sckitlearn

# the problem
# - divide data into two distinct categories along side a boundary line
# that separates the classesself.
# Data Source
# https://www.kaggle.com/uciml/pima-indians-diabetes-database/data
# https://www.kaggle.com/uciml/pima-indians-diabetes-database/downloads/diabetes.csv/1

import matplotlib
matplotlib.use ('pdf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
import csv

# url = "https://www.kaggle.com/uciml/pima-indians-diabetes-database/downloads/diabetes.csv"
# response = urlopen(url)
# print(response.read().decode('utf-8'))

dataset = pd.read_csv("pima-indians-diabetes.csv", comment="#", header=0)
print ("Take a peek at the data")
print("Shape: ", dataset.shape)
print("Head: ", dataset.head())
print("Describe:", dataset.describe())
print()



corr = dataset.corr()#first check correlation amongst the features
fig,ax = plt.subplots(figsize=(13,13))
ax.matshow(corr) # color code the rectatgles by correlation

plt.xticks(range(len(corr.columns)), corr.columns) # tick marks
plt.yticks(range(len(corr.columns)), corr.columns)

plt.savefig("/tmp/outfig.pdf",  bbox_inches='tight')

features = dataset.drop(['Outcome'], axis=1) #separate our columns into features & labels
labels = dataset['Outcome']

from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.25)

# import the model
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier()
classifier.fit(features_train, labels_train)

pred = classifier.predict(features_test)

# Assess performance
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(labels_test, pred)
print ('accuracy: {}'.format(accuracy))
