"""Get Scores and Run Classifiers"""
import pickle

from sklearn import decomposition
from sklearn.metrics import mean_absolute_error, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd


def get_score(model, x_train, y_train, x_test, y_test, name):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    # Determine Mean Absolute Error/Score
    print(name + "(MAE)", mean_absolute_error(y_test, predictions))
    print(name + "(Score)", model.score(x_test, y_test))


# Prepare the X, y variables
def prepare_variables(df, dependent_variable):
    print("Preparing Variables")
    df[dependent_variable] = df[dependent_variable].astype('int')
    Y = df[dependent_variable]

    X = df.drop([dependent_variable], axis=1)
    X = pd.get_dummies(X)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=1)

    return X_train, X_test, Y_train, Y_test


# Determine Best Parameters
def grid_search(X_train, Y_train, X_test, Y_test, model_name, classifier, parameter_list):
    print("Running Classifiers")
    sc = StandardScaler()
    pca = decomposition.PCA()

    pipe = Pipeline(steps=[('sc', sc),
                           ('pca', pca),
                           (model_name, classifier)])

    # Dictionary of Parameter options
    parameters = parameter_list

    # Optimize Parameters
    clf = GridSearchCV(pipe, parameters)

    # Grid Search
    clf.fit(X_train, Y_train)

    # Print Best Parameters
    print('Best Criteria:', clf.best_estimator_.get_params()[model_name + '__criterion'])
    print('Best max_depth:', clf.best_estimator_.get_params()[model_name + '__max_depth'])
    print('Best Number Of Components:', clf.best_estimator_.get_params()['pca__n_components'])

    print(clf.best_estimator_.get_params()[model_name])

    # Cross Validation
    CV_Result = cross_val_score(clf, X_train, Y_train, cv=4, n_jobs=-1)
    print(CV_Result)
    print(CV_Result.mean())
    print(CV_Result.std())

    # Precision, Recall, F1
    prediction = clf.predict(X_test)
    print(confusion_matrix(Y_test, prediction))
    print(classification_report(Y_test, prediction))
