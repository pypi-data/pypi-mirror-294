import numpy as np
import pandas as pd
import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, confusion_matrix as cm

def run_nbclassifier():
    
    wine = datasets.load_wine()

    print("Features: ", wine.feature_names)
    print("Labels: ", wine.target_names)

    X = pd.DataFrame(wine['data'])

    print(X.head())
    print(wine.data.shape)

    y = wine.target
    print(y)

    X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.30, random_state=109)

    gnb = GaussianNB()

    gnb.fit(X_train, y_train)

    y_pred = gnb.predict(X_test)
    print(y_pred)

    print("Accuracy:", accuracy_score(y_test, y_pred))

    print("Confusion Matrix:\n", cm(y_test, y_pred))


if __name__ == "__main__":
    run_nbclassifier()