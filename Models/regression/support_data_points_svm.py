import matplotlib
matplotlib.use ('pdf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("pima-indians-diabetes.csv", comment="#", header=0)
# create features and labels
features = dataset.drop(['Outcome'], axis=1)
labels  = dataset['Outcome']

# split dataset into training and test sets
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.25)

# import svm classifier
# SVC linear, poly, rbf, sigmoid, precomputed,
from sklearn.svm import SVC
classifier= SVC(kernel='linear')

## Common
classifier.fit(features_train, labels_train)

pred = classifier.predict(features_test)

# Assess performance
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(labels_test, pred)
print ('accuracy: {}'.format(accuracy))
