# -*- coding: utf-8 -*-
"""Customer_churn_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kd0Bw22VrotLjG6sYdGwaT1JGLvUusd-
"""

#import all the important libraries required for developing the model.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import confusion_matrix,classification_report

#reading the dataset with the help of pandas library.
churn = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/Churn_Modelling.csv")

##displaying first five rows of the dataframe using the head command
churn.head(5)

#countplot of the exited customers represented by 1 and represented by 0 those who are not exited.
sns.countplot(x = 'Exited', data = churn)

#pairplot of the dataset
sns.pairplot(churn, hue = 'Exited')

#dropping the unwanted labels
churn = churn.drop(labels = {'Gender', 'Geography', 'Surname'}, axis = 1)

#info of the dataset
churn.info()

#displaying the columns
churn.columns

#features to be selected as predictors
selected_features = ['RowNumber', 'CustomerId', 'CreditScore', 'Age', 'Tenure', 'Balance',
       'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']

#taking X as predictor and y as target variable.
X = churn[selected_features]
y = churn['Exited']

#normalizing the dataset using MinMaxScaler()
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled

#displaying the shape of predictor and target variables
print(X.shape)
print(y.shape)

#Splitting the dataset into training and testing sets
X_train,X_test,y_train,y_test = train_test_split(X_scaled, y, test_size = 0.2)

#displaying the shape of training and testing sets
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#imported the LogisticRegression() algorithm through sklearn and fitted the
#training dataset into and evaluated the model on the testing set
model1 = LogisticRegression()
model1.fit(X_train,y_train)
print("Training_Score:",model1.score(X_train, y_train)*100)
print("Testing_score :",model1.score(X_test, y_test)*100)

#imported the RandomForestClassifier() algorithm through sklearn and fitted the
#training dataset into and evaluated the model on the testing set
model2 = RandomForestClassifier()
model2.fit(X_train,y_train)
print("Training_Score:",model2.score(X_train, y_train)*100)
print("Testing_score :",model2.score(X_test, y_test)*100)

#imported the XGBClassifier() algorithm through sklearn and fitted the
#training dataset into and evaluated the model on the testing set
model3 = xgb.XGBClassifier()
model3.fit(X_train,y_train)
print("Training_Score:",model3.score(X_train, y_train)*100)
print("Testing_score :",model3.score(X_test, y_test)*100)

#imported Ann through keras API and tensorflow
#ANN is just to check how it performs on the dataset.
classifier_model = tf.keras.models.Sequential()
classifier_model.add(tf.keras.layers.Dense(units = 100, activation = 'relu', input_shape = (10,)))
classifier_model.add(tf.keras.layers.Dropout(0.3))
classifier_model.add(tf.keras.layers.Dense(units = 50, activation = 'relu'))
classifier_model.add(tf.keras.layers.Dropout(0.3))
classifier_model.add(tf.keras.layers.Dense(units = 50, activation = 'relu'))
classifier_model.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

#compiled Ann model
classifier_model.compile(optimizer = 'Adam', loss = 'binary_crossentropy', metrics = 'accuracy')

#calculating the epochs on training dataset
epochs_hist = classifier_model.fit(X_train,y_train,epochs = 50,batch_size = 125)

#finding out the keys of epochs
epochs_hist.history.keys()

#plotting the graph between the training loss and accuracy vs number epochs.
eh = epochs_hist.history['loss']
eh2 = epochs_hist.history['accuracy']
plt.plot(eh)
plt.plot(eh2)
plt.title('Training loss and Accuracy vs epochs graph')
plt.xlabel('epochs')
plt.ylabel('Training loss and Accuracy')
plt.legend({'accuracy', 'loss'})

#evaluating the model on the testing dataset.
evaluation = classifier_model.evaluate(X_test,y_test)
print('test accuracy:{}'.format(evaluation[1]))

#prediction of the model
#model2 is RandomForestClassifier()
y_predict = model2.predict(X_test)

#displaying the predicted values
y_predict

#filtering those values greater than 0.5 in testing dataset.
y_predict = (y_predict > 0.5)
y_predict

#predict the values on the training test
#model2 is RandomForestClassifier()
y_train_predict = model2.predict(X_train)

#filtering those values greater than 0.5 in training dataset.
y_train_predict =  (y_train_predict > 0.5)

y_train_predict

#plotting the confusion matrix of training dataset
from sklearn.metrics import confusion_matrix,classification_report
cm = confusion_matrix(y_train, y_train_predict)
sns.heatmap(cm, annot = True)

#plotting the confusion matrix of testing dataset
cm2 = confusion_matrix(y_test, y_predict)
sns.heatmap(cm2, annot = True)

#printing the classification report of training and testing dataset
print("Training Report:\n",classification_report(y_train,y_train_predict))
print("Testing Report:\n",classification_report(y_test, y_predict))