import numpy as np
from sklearn.datasets import load_diabetes


def get_data(n_clients):
    """Returns train and test dataset split for each client

    Args:
        n_clients (int): number of clients

    Returns:
        X (list[NDarray]): list of train data
        y (list[NDarray]): list of train label
        X_test (list[NDarray]): list of test data
        y_test (list[NDarray]): list of test label
    """

    # Seed for reproductability
    seed = 42
    np.random.seed(seed)

    diabetes = load_diabetes()
    y = diabetes.target
    X = diabetes.data

    # Add constant to emulate intercept
    X = np.c_[X, np.ones(X.shape[0])]

    # The features are already preprocessed
    # Shuffle
    # Is this really useful ? As the representative test set is already sampled randomly (see below)
    # and that we want to induce a bias on the splited distributions ?
    perm = np.random.permutation(X.shape[0])
    X, y = X[perm, :], y[perm]

    # Select test at random
    test_size = 50
    test_idx = np.random.choice(X.shape[0], size=test_size, replace=False)
    train_idx = np.ones(X.shape[0], dtype=bool)
    train_idx[test_idx] = False
    X_test, y_test = X[test_idx, :], y[test_idx]
    X_train, y_train = X[train_idx, :], y[train_idx]

    # Split train among multiple clients.
    # The selection is not at random but by slice. We simulate the fact that each client
    # sees a potentially very different sample of patients. ??? Not really because the original dataset has been suffled.
    X, y = [], []
    step = int(X_train.shape[0] / n_clients)
    for c in range(n_clients):
        X.append(X_train[step * c: step * (c + 1), :])
        y.append(y_train[step * c: step * (c + 1)])

    return X, y, X_test, y_test

def mean_square_error(y_pred, y):
    return np.mean((y - y_pred) ** 2)
