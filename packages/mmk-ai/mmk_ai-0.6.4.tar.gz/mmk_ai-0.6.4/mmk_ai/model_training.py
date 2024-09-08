from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import optuna
import joblib

def train_model_threaded(X_train, X_test, y_train, y_test, model_name):
    """
    Trains a specified machine learning model and returns its performance on the test set.
    """
    models = {
        "RandomForestClassifier": RandomForestClassifier(),
        "GradientBoostingClassifier": GradientBoostingClassifier(),
        "SVC": SVC(probability=True),
        "LogisticRegression": LogisticRegression(),
        "KNeighborsClassifier": KNeighborsClassifier(),
        "DecisionTreeClassifier": DecisionTreeClassifier(),
        "AdaBoostClassifier": AdaBoostClassifier(),
        "BaggingClassifier": BaggingClassifier(),
        "ExtraTreesClassifier": ExtraTreesClassifier(),
        "RidgeClassifier": RidgeClassifier(),
        "SGDClassifier": SGDClassifier(),
        "GaussianNB": GaussianNB(),
        "BernoulliNB": BernoulliNB(),
        "LinearDiscriminantAnalysis": LinearDiscriminantAnalysis(),
        "QuadraticDiscriminantAnalysis": QuadraticDiscriminantAnalysis(),
        "MLPClassifier": MLPClassifier(),
        "GaussianProcessClassifier": GaussianProcessClassifier(),
        "ExtraTreeClassifier": ExtraTreeClassifier()
    }

    model = models.get(model_name)
    if model:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        if model_name.endswith('Classifier'):
            score = accuracy_score(y_test, y_pred)
        else:
            score = model.score(X_test, y_test)

        return model, score
    else:
        raise ValueError(f"Model {model_name} is not supported.")

def save_model(model, file_path):
    """
    Saves a trained model to a specified file path using joblib.
    """
    joblib.dump(model, file_path)

def load_model(file_path):
    """
    Loads a trained model from a specified file path using joblib.
    """
    return joblib.load(file_path)

def objective(trial, X_train, y_train):
    """
    Objective function for optimizing model hyperparameters using Optuna.
    """
    model_name = trial.suggest_categorical('model_name', [
        'RandomForestClassifier',
        'GradientBoostingClassifier',
        'SVC',
        'LogisticRegression',
        'KNeighborsClassifier',
        'DecisionTreeClassifier',
        'AdaBoostClassifier',
        'BaggingClassifier',
        'ExtraTreesClassifier',
        'RidgeClassifier',
        'SGDClassifier',
        'GaussianNB',
        'BernoulliNB',
        'LinearDiscriminantAnalysis',
        'QuadraticDiscriminantAnalysis',
        'MLPClassifier',
        'GaussianProcessClassifier',
        'ExtraTreeClassifier'
    ])

    models = {
        "RandomForestClassifier": RandomForestClassifier,
        "GradientBoostingClassifier": GradientBoostingClassifier,
        "SVC": SVC,
        "LogisticRegression": LogisticRegression,
        "KNeighborsClassifier": KNeighborsClassifier,
        "DecisionTreeClassifier": DecisionTreeClassifier,
        "AdaBoostClassifier": AdaBoostClassifier,
        "BaggingClassifier": BaggingClassifier,
        "ExtraTreesClassifier": ExtraTreesClassifier,
        "RidgeClassifier": RidgeClassifier,
        "SGDClassifier": SGDClassifier,
        "GaussianNB": GaussianNB,
        "BernoulliNB": BernoulliNB,
        "LinearDiscriminantAnalysis": LinearDiscriminantAnalysis,
        "QuadraticDiscriminantAnalysis": QuadraticDiscriminantAnalysis,
        "MLPClassifier": MLPClassifier,
        "GaussianProcessClassifier": GaussianProcessClassifier,
        "ExtraTreeClassifier": ExtraTreeClassifier
    }

    model_class = models.get(model_name)

    if model_name == 'RandomForestClassifier':
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 200),
            'max_depth': trial.suggest_int('max_depth', 2, 32)
        }

    elif model_name == 'GradientBoostingClassifier':
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 200),
            'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.3)
        }

    elif model_name == 'SVC':
        params = {
            'C': trial.suggest_loguniform('C', 1e-10, 1e10),
            'kernel': trial.suggest_categorical('kernel', ['linear', 'poly', 'rbf', 'sigmoid'])
        }

    elif model_name == 'LogisticRegression':
        params = {
            'C': trial.suggest_loguniform('C', 1e-10, 1e10),
            'solver': trial.suggest_categorical('solver', ['newton-cg', 'lbfgs', 'liblinear'])
        }

    elif model_name == 'KNeighborsClassifier':
        params = {
            'n_neighbors': trial.suggest_int('n_neighbors', 2, 40)
        }

    elif model_name == 'DecisionTreeClassifier':
        params = {
            'max_depth': trial.suggest_int('max_depth', 2, 32),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy'])
        }

    elif model_name == 'AdaBoostClassifier':
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 200)
        }

    elif model_name == 'BaggingClassifier':
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 200)
        }

    elif model_name == 'ExtraTreesClassifier':
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 200),
            'max_depth': trial.suggest_int('max_depth', 2, 32)
        }

    elif model_name == 'RidgeClassifier':
        params = {
            'alpha': trial.suggest_loguniform('alpha', 1e-10, 1e10)
        }

    elif model_name == 'SGDClassifier':
        params = {
            'alpha': trial.suggest_loguniform('alpha', 1e-10, 1e10),
            'max_iter': trial.suggest_int('max_iter', 1000, 5000)
        }

    elif model_name == 'MLPClassifier':
        params = {
            'hidden_layer_sizes': trial.suggest_categorical('hidden_layer_sizes', [(50,), (100,), (50, 50)]),
            'activation': trial.suggest_categorical('activation', ['tanh', 'relu']),
            'learning_rate_init': trial.suggest_loguniform('learning_rate_init', 1e-4, 1e-1),
            'max_iter': trial.suggest_int('max_iter', 200, 1000)
        }

    elif model_name == 'GaussianProcessClassifier':
        params = {}

    elif model_name == 'ExtraTreeClassifier':
        params = {
            'max_depth': trial.suggest_int('max_depth', 2, 32),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy'])
        }

    elif model_name in ['GaussianNB', 'BernoulliNB', 'LinearDiscriminantAnalysis', 'QuadraticDiscriminantAnalysis']:
        params = {}

    model = model_class(**params)
    score = cross_val_score(model, X_train, y_train, n_jobs=-1, cv=3)
    accuracy = score.mean()
    return accuracy

def optimize_hyperparameters(X_train, y_train, n_trials=50):
    """
    Optimizes the hyperparameters of a model using Optuna.
    """
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=n_trials)

    print("Best model:", study.best_trial.params)
    return study.best_trial.params
