import concurrent.futures
import csv
from mmk_ai.data_preprocessing import preprocess_data, load_csv
from mmk_ai.model_training import train_model_threaded, optimize_hyperparameters, save_model

def auto_train(data_path, target_column, model_names, save_model_paths=None, csv_export_paths=None, n_trials=50):
    """
    Automatically trains multiple machine learning models on a dataset, 
    optimizes hyperparameters using Optuna, and optionally saves the models and their results.
    
    Parameters:
    -----------
    data_path : str
        The file path of the dataset in CSV format.
    target_column : str
        The name of the target column in the dataset.
    model_names : list
        List of model names to train. 
        Available models: 'RandomForestClassifier', 'GradientBoostingClassifier', 'SVC', 
                          'LogisticRegression', 'KNeighborsClassifier', 'DecisionTreeClassifier',
                          'AdaBoostClassifier', 'BaggingClassifier', 'ExtraTreesClassifier',
                          'RidgeClassifier', 'SGDClassifier', 'GaussianNB', 'BernoulliNB',
                          'LinearDiscriminantAnalysis', 'QuadraticDiscriminantAnalysis',
                          'MLPClassifier', 'GaussianProcessClassifier', 'ExtraTreeClassifier'
    save_model_paths : dict, optional
        Dictionary of model names as keys and file paths as values where the trained models will be saved.
    csv_export_paths : dict, optional
        Dictionary of model names as keys and file paths as values where the results will be exported as CSV.
    n_trials : int, optional
        The number of trials for hyperparameter optimization. Default is 50.

    Returns:
    --------
    dict
        A dictionary containing the trained models and their performance scores.

    Example:
    --------
    >>> results = auto_train("data.csv", "target", ["RandomForestClassifier", "SVC"])
    >>> print(results)
    """

    # Step 1: Load and preprocess the data
    data = load_csv(data_path)
    X_train, X_test, y_train, y_test = preprocess_data(data, target_column)

    # Step 2: Optimize hyperparameters for each model
    best_params = {}
    for model_name in model_names:
        print(f"Optimizing hyperparameters for {model_name}...")
        best_params[model_name] = optimize_hyperparameters(X_train, y_train, n_trials=n_trials)

    # Step 3: Train each model in parallel using ThreadPoolExecutor
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_model = {
            executor.submit(
                train_model_threaded, X_train, X_test, y_train, y_test, model_name, best_params[model_name]
            ): model_name for model_name in model_names
        }
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                model, score = future.result()
                results[model_name] = {
                    "model": model,
                    "score": score
                }
                print(f"{model_name} Training Completed. Score: {score}")

                # Step 4: Save the trained model
                if save_model_paths and model_name in save_model_paths:
                    save_model(model, save_model_paths[model_name])

                # Step 5: Export results to CSV
                if csv_export_paths and model_name in csv_export_paths:
                    print(f"Exporting results for {model_name} to {csv_export_paths[model_name]}...")
                    with open(csv_export_paths[model_name], mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Metric', 'Score'])
                        writer.writerow(['Accuracy', score])
            except Exception as exc:
                print(f"{model_name} generated an exception: {exc}")

    return results
