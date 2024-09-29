import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import random

data = pd.read_csv('2020_bn_nb_data.txt', sep='\t') 

print(data.head())

def calculate_cpts(data):
    cpts = {}
    for course in data.columns[:-1]:  
        cpts[course] = data[course].value_counts(normalize=True).to_dict()
    return cpts

cpts = calculate_cpts(data)

def predict_ph100(ec100_grade, it101_grade, ma101_grade, cpts):
   
    ph100_probs = cpts['PH100']
    return ph100_probs  

ec100_grade = 'DD'
it101_grade = 'CC'
ma101_grade = 'CD'
ph100_prediction = predict_ph100(ec100_grade, it101_grade, ma101_grade, cpts)
print(f"Predicted probabilities for PH100 given grades: {ph100_prediction}")

X = data.iloc[:, :-1]  
y = data.iloc[:, -1]  

accuracies = []

for _ in range(20): 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random.randint(0, 100))
    
    model = GaussianNB()
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    accuracies.append(accuracy)

print(f"Accuracies from 20 random selections: {accuracies}")
print(f"Mean accuracy: {np.mean(accuracies)}")
print(f"Standard deviation of accuracies: {np.std(accuracies)}")
