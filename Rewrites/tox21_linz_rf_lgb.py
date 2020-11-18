# make sure  numpy, scipy, pandas, sklearn are installed, otherwise run
# pip install numpy scipy pandas scikit-learn
import numpy as np
import pandas as pd
from scipy import io
import lightgbm as lgb

from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score

def lgb_f1_score(y_hat, data):
    y_true = data.get_label()
    y_hat = np.round(y_hat) # scikits f1 doesn't like probabilities
    return 'f1', f1_score(y_true, y_hat), True


def train_estimator_with_model(est: str ,
                               train_x, train_y,
                               test__x, test__y):
    '''returns a trained model'''
    if est == 'lightgbm':
        mdl = lightgbm_estimator(train_x, train_y,
                               test__x, test__y)
        return mdl
    elif est == 'random_forest':
        mdl = random_forest_estimator(train_x, train_y,
                               test__x, test__y)
        return mdl
    else:
        return

def random_forest_estimator(X_train, y_train, X_test, y_test):
    rf = RandomForestClassifier(n_estimators=100,  n_jobs=4)
    rf.fit(X_train, y_train)
    return rf
    
def lightgbm_estimator(X_train, y_train, X_test, y_test):
    evals_result = {}

    num_train, num_feature = X_train.shape

    # create dataset for lightgbm
    # if you want to re-use data, remember to set free_raw_data=False
    lgb_train = lgb.Dataset(X_train, y_train
#                            weight=W_train
                            , free_raw_data=False)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train,
                           free_raw_data=False)

    # specify your configurations as a dict
    params = {
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': 'auc',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }

    # generate feature names
    feature_name = ['feature_' + str(col) for col in range(num_feature)]

    print('Starting training...')
    # feature_name and categorical_feature
#    clf = lgb.train(param, train_data, valid_sets=[val_data, train_data], valid_names=['val', 'train'], feval=lgb_f1_score, evals_result=evals_result)

    gbm = lgb.train(params,
                    lgb_train,
                    #num_boost_round=10,
                    valid_sets=lgb_train,  # eval training data
                    feature_name=feature_name,
                    verbose_eval=False,
                    feval=lgb_f1_score
                    , evals_result=evals_result)
#                    categorical_feature=[21])

    lgb.plot_metric(evals_result, metric='f1')
    print('Finished first k rounds...')
    
    return gbm

# load data

y_tr = pd.read_csv('tox21_labels_train.csv.gz', index_col=0, compression="gzip")
y_te = pd.read_csv('tox21_labels_test.csv.gz', index_col=0, compression="gzip")
x_tr_dense = pd.read_csv('tox21_dense_train.csv.gz', index_col=0, compression="gzip").values
x_te_dense = pd.read_csv('tox21_dense_test.csv.gz', index_col=0, compression="gzip").values
x_tr_sparse = io.mmread('tox21_sparse_train.mtx.gz').tocsc()
x_te_sparse = io.mmread('tox21_sparse_test.mtx.gz').tocsc()

# filter out very sparse features
from matplotlib import pyplot
from sklearn.metrics import roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, roc_auc_score


sparse_col_idx = ((x_tr_sparse > 0).mean(0) > 0.05).A.ravel()
x_tr = np.hstack([x_tr_dense])
x_te = np.hstack([x_te_dense])


# Build a random forest model for all twelve assays
results =[]
for target in y_tr.columns:
    rows_tr = np.isfinite(y_tr[target]).values
    rows_te = np.isfinite(y_te[target]).values
#    est = RandomForestClassifier(n_estimators=100,  n_jobs=4)
#    est = GradientBoostingClassifier(random_state=0)
#    est.fit(x_tr[rows_tr], y_tr[target][rows_tr])
    est = train_estimator_with_model( \
                             'lightgbm',
                             x_tr[rows_tr], y_tr[target][rows_tr],
                             x_te[rows_te], y_te[target][rows_te])
    p_te = est.predict(x_te[rows_te])
    pos_probs = p_te
    auc_te = roc_auc_score(y_te[target][rows_te], pos_probs)
    fpr, tpr, thresholds = roc_curve(y_te[target][rows_te], pos_probs)
    results.append(["%20s: %3.3f" % (target, auc_te)])
    # todo what is: print(thresholds)?

[print(x) for x in results]
#pyplot.plot(fpr, tpr, marker='.', label='Random Forest')
## axis labels
#pyplot.xlabel('False Positive Rate')
#pyplot.ylabel('True Positive Rate')
## show the legend
#pyplot.legend()
## show the plot
pyplot.show()

