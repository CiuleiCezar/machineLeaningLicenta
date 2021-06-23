import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pickle
import requests
import json

# Importing the dataset
dataset = pd.read_csv('Salary_Data.csv')
diabetes_data = pd.read_csv('diabetes.csv')

diabetes_data_copy = diabetes_data.copy(deep=True)
diabetes_data_copy[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = diabetes_data_copy[
    ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']].replace(0, np.NaN)

diabetes_data_copy['Glucose'].fillna(diabetes_data_copy['Glucose'].mean(), inplace=True)
diabetes_data_copy['BloodPressure'].fillna(diabetes_data_copy['BloodPressure'].mean(), inplace=True)
diabetes_data_copy['SkinThickness'].fillna(diabetes_data_copy['SkinThickness'].median(), inplace=True)
diabetes_data_copy['Insulin'].fillna(diabetes_data_copy['Insulin'].median(), inplace=True)
diabetes_data_copy['BMI'].fillna(diabetes_data_copy['BMI'].median(), inplace=True)

sc_X = StandardScaler()
X = pd.DataFrame(sc_X.fit_transform(diabetes_data_copy.drop(["Outcome"], axis=1), ),
                 columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
                          'BMI', 'DiabetesPedigreeFunction', 'Age'])
y = diabetes_data_copy.Outcome

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=42, stratify=y)

test_scores = []
train_scores = []

for i in range(1, 15):
    knn = KNeighborsClassifier(i)
    knn.fit(X_train, y_train)

    train_scores.append(knn.score(X_train, y_train))
    test_scores.append(knn.score(X_test, y_test))

max_train_score = max(train_scores)
train_scores_ind = [i for i, v in enumerate(train_scores) if v == max_train_score]
print('Max train score {} % and k = {}'.format(max_train_score * 100, list(map(lambda x: x + 1, train_scores_ind))))

knn = KNeighborsClassifier(11)

knn.fit(X_train, y_train)
aux = knn.score(X_test, y_test)
print(aux)

pickle.dump(knn, open('modelKnn.pkl', 'wb'))

model = pickle.load(open('modelKnn.pkl', 'rb'))
print(model.predict([[1, 1, 1, 1, 1, 1, 1, 1]]))

# X = dataset.iloc[:, :-1].values
# y = dataset.iloc[:, 1].values
#
# # Splitting the dataset into the Training set and Test set
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
#
# regressor = LinearRegression()
# regressor.fit(X_train, y_train)
#
# # Predicting the Test set results
# y_pred = regressor.predict(X_test)
# # Saving model to disk
# pickle.dump(regressor, open('model.pkl','wb'))
# # Loading model to compare the results
# model = pickle.load(open('model.pkl','rb'))
# print(model.predict([[1.8]]))
