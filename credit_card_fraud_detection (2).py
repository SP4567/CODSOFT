# -*- coding: utf-8 -*-
"""Credit_Card_Fraud_Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wdJRHy_6i2OlqPSnqueDo6GOx2Nhf_o6
"""

#importing all the important libraries required for developing the model.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
import tensorflow as tf
from sklearn.metrics import confusion_matrix,classification_report

#reading the dataset with the help of pandas library.
tr = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/fraudTrain.csv')
tt = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/fraudTest.csv')

#displaying first five rows of the dataframe using the head command
tr.head(5)#training dataset

#displaying first five rows of the dataframe using the head command
tt.head(5)#testing dataset

#countplot of the isfraud represented by 1 and represented by 0 for not fraud.
sns.countplot(x = 'is_fraud', data = tr)#training dataset

#countplot of the isfraud represented by 1 and represented by 0 for not fraud.
sns.countplot(x = 'is_fraud', data = tt)#testing dataset

#dropping the unwanted labels
tr = tr.drop(labels={'trans_date_trans_time','category', 'street'}, axis = 1)

#info of the training dataset
tr.info()

#filling the empty cells with fillna method in training dataset.
tr['dob']= tr['dob'].fillna(method = 'ffill')
tr['trans_num']= tr['trans_num'].fillna(method = 'ffill')
tr['unix_time']= tr['unix_time'].fillna(method = 'ffill')
tr['merch_lat']= tr['merch_lat'].fillna(method = 'ffill')
tr['merch_long']= tr['merch_long'].fillna(method = 'ffill')
tr['is_fraud']= tr['is_fraud'].fillna(method = 'ffill')

#info of the training data after removing the unwanted labels and filling the empty cells.
tr.info()

#info of the testing data
tt.info()

#dropping the unwanted labels
tt = tt.drop(labels={'trans_date_trans_time','category', 'street'}, axis = 1)

#filling the empty cells with fillna method in testing dataset.
tt['dob']= tt['dob'].fillna(method = 'ffill')
tt['trans_num']= tt['trans_num'].fillna(method = 'ffill')
tt['unix_time']= tt['unix_time'].fillna(method = 'ffill')
tt['merch_lat']= tt['merch_lat'].fillna(method = 'ffill')
tt['merch_long']= tt['merch_long'].fillna(method = 'ffill')
tt['is_fraud']= tt['is_fraud'].fillna(method = 'ffill')
tt['job']= tt['job'].fillna(method = 'ffill')
tt['city_pop']= tt['city_pop'].fillna(method = 'ffill')

#info of the testing data after removing the unwanted labels and filling empty cells.
tt.info()

#features to be selected as predictors.Taking X as predictor and y as target variable in training dataset
selected_features = {'cc_num', 'amt', 'zip', 'lat', 'long', 'city_pop', 'unix_time', 'merch_lat', 'merch_long'}
X_train = tr[selected_features]
y_train = tr['is_fraud']

#normalizing the training dataset using MinMaxScaler()
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)

#features to be selected as predictors.Taking X as predictor and y as target variable in testing dataset
selected_features2 = {'cc_num', 'amt', 'zip', 'lat', 'long', 'city_pop', 'unix_time', 'merch_lat', 'merch_long'}
X_test = tt[selected_features]
y_test = tt['is_fraud']

#normalizing the testing dataset using MinMaxScaler()
X_test = scaler.fit_transform(X_test)

#displaying the shape of training and testing sets
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#imported the LogisticRegression() algorithm through sklearn and fitted the
#training dataset into and evaluated the model on the testing set
model2 = LogisticRegression()
model2.fit(X_train, y_train)
print("Training_Score:",model2.score(X_train, y_train)*100)
print("Testing_score :",model2.score(X_test, y_test)*100)

#imported the GaussianNB() algorithm through sklearn and fitted the
#training dataset into and evaluated the model on the testing set
model3 = GaussianNB()
model3.fit(X_train, y_train)
print("Training_Score:",model3.score(X_train, y_train)*100)
print("Testing_score :",model3.score(X_test, y_test)*100)

#imported the RandomForestClassifier() algorithm through sklearn and fitted the
#training dataset into and evaluated the model on the testing set
model4 = RandomForestClassifier()
model4.fit(X_train, y_train)
print("Training_Score:",model4.score(X_train, y_train)*100)
print("Testing_score :",model4.score(X_test, y_test)*100)

#imported Ann through keras API and tensorflow
#ANN is just to check how it performs on the dataset.
classifier_model = tf.keras.models.Sequential()
classifier_model.add(tf.keras.layers.Dense(units = 64, activation = 'relu', input_shape = (9,)))
classifier_model.add(tf.keras.layers.Dropout(0.3))
classifier_model.add(tf.keras.layers.Dense(units = 32, activation = 'relu'))
classifier_model.add(tf.keras.layers.Dropout(0.3))
classifier_model.add(tf.keras.layers.Dense(units = 32, activation = 'relu'))
classifier_model.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

#compiled Ann model
classifier_model.compile(optimizer = 'Adam', loss = 'binary_crossentropy', metrics = 'accuracy')

#calculating the epochs on training dataset
epochs_hist = classifier_model.fit(X_train,y_train, epochs = 5, batch_size = 125)

#finding out the keys of epochs
epochs_hist.history.keys()

#plotting the graph between the training loss and accuracy vs number epochs.
eh = epochs_hist.history['accuracy']
eh2 = epochs_hist.history['loss']
plt.plot(eh)
plt.plot(eh2)
plt.title('Accuracy and Loss vs epochs Graph')
plt.xlabel('epochs')
plt.ylabel('Accuracy and Loss')
plt.legend({'accuracy','loss'})

#evaluating the model on the testing dataset.
evaluation = classifier_model.evaluate(X_test, y_test)
print('test_accuracy:{}'.format(evaluation[1]))

#prediction of the model.model3 is GaussainNB().
y_predict = model3.predict(X_test)

#displaying the predicted values
print(y_predict)

#prediction of the model.
y_predict = (y_predict > 0.5)

#displaying the predicted values
y_predict

#filtering those values greater than 0.5 in training dataset.model3 is GaussainNB().
y_train_predict = model3.predict(X_train)
y_train_predict = (y_train_predict > 0.5)

#displaying the predicted values of the training dataset
y_train_predict

#plotting the confusion matrix of training dataset
cm = confusion_matrix(y_train, y_train_predict)
sns.heatmap(cm, annot = True)

#plotting the confusion matrix of testing dataset
cm2 = confusion_matrix(y_test, y_predict)
sns.heatmap(cm2, annot = True)

#printing the classification report of training and testing dataset
print("Training Report:\n",classification_report(y_train,y_train_predict))
print("Testing Report:\n",classification_report(y_test, y_predict))

