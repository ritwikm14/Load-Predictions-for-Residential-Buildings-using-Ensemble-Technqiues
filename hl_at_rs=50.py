# -*- coding: utf-8 -*-
"""HL at rs=50.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VsmlUs7epimMlJ6gwTByAm0Z76OgWIed
"""

import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
!pip install scikit-optimize
from skopt import BayesSearchCV
from skopt.space import Real, Integer
from scipy.stats import pearsonr

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00242/ENB2012_data.xlsx'
df = pd.read_excel(url)
df.columns = ['Relative_Compactness', 'Surface_Area', 'Wall_Area', 'Roof_Area', 'Overall_Height',
              'Orientation', 'Glazing_Area', 'Glazing_Area_Distribution', 'Heating_Load', 'Cooling_Load']

# Drop Cooling_Load from the dataframe
df.drop(['Cooling_Load'], axis=1, inplace=True)
df.head()

train_data, test_data, train_target, test_target = train_test_split(df.iloc[:, :-1], df.iloc[:, -1],
                                                                    test_size=0.3, random_state=50)

xgb_model = xgb.XGBRegressor(
    objective='reg:squarederror',
    booster='gbtree',
    n_jobs=-1,
    random_state=50
)
search_space = {
    'learning_rate': Real(0.01, 0.1, prior='log-uniform'),
    'max_depth': Integer(3, 10),
    'n_estimators': Integer(50, 500),
    'gamma': Real(0, 1),
    'subsample': Real(0.5, 1),
    'colsample_bytree': Real(0.5, 1),
    'reg_alpha': Real(0, 10),
    'reg_lambda': Real(0, 10)
}

bayes_cv_tuner = BayesSearchCV(
    estimator=xgb_model,
    search_spaces=search_space,
    scoring='neg_mean_squared_error',
    n_iter=50,
    cv=5,
    verbose=1,
    random_state=50,
    n_jobs=-1
)

bayes_cv_tuner.fit(train_data, train_target)

xgb_opt = BayesSearchCV(
    xgb_model,
    search_space,
    cv=5,
    n_iter=50,
    n_jobs=-1,
    random_state=50
)
xgb_opt.fit(train_data, train_target)

# Print the best hyperparameters
print("Best hyperparameters found by Bayesian optimization search:")
print(xgb_opt.best_params_)

xgb_model = xgb.XGBRegressor(
    objective='reg:squarederror',
    booster='gbtree',
    n_jobs=-1,
    random_state=50,
    **bayes_cv_tuner.best_params_
)
xgb_model.fit(train_data, train_target)
test_preds = xgb_model.predict(test_data)
train_preds = xgb_model.predict(train_data)

train_mse = mean_squared_error(train_target, train_preds)
train_rmse = mean_squared_error(train_target, train_preds, squared=False)
train_r2 = r2_score(train_target, train_preds)

test_rmse = mean_squared_error(test_target, test_preds, squared=False)
test_mse = mean_squared_error(test_target, test_preds)
test_mae = mean_absolute_error(test_target, test_preds)
test_r2 = r2_score(test_target, test_preds)

print(f"Test RMSE: {test_rmse:.2f}")
print(f"Test MSE: {test_mse:.2f}")
print(f"Test MAE: {test_mae:.2f}")
print(f"Test R^2: {test_r2:.2f}")
print(f"Train MSE: {train_mse:.2f}")
print(f"Train RMSE: {train_rmse:.2f}")
print(f"Train R^2: {train_r2:.2f}")

from sklearn.ensemble import RandomForestRegressor
!pip install scikit-optimize
from skopt.space import Real, Integer, Categorical

# Define the hyperparameter search space for the random forest model
search_space = {
    'n_estimators': Integer(100, 500),
    'max_depth': Integer(1, 50),
    'min_samples_split': Integer(2, 10),
    'min_samples_leaf': Integer(1, 10),
    'max_features': Categorical(['sqrt', 'log2', None]),
    'bootstrap': Categorical([True, False])
}

# Define the Bayesian optimization object
rf_bo = BayesSearchCV(
    RandomForestRegressor(random_state=50),
    search_space,
    n_iter=32,
    cv=5,
    random_state=50
)

# Fit the Bayesian optimization object to the training data
rf_bo.fit(train_data, train_target)

print("Best Hyperparameters for Random Forest Regressor: ", rf_bo.best_params_)

import numpy as np
# Evaluate the model on the testing set
test_pred = rf_bo.predict(test_data)
mse = mean_squared_error(test_target, test_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(test_target, test_pred)
r2 = r2_score(test_target, test_pred)
print("Evaluation metrics on Test Set:")
print("MSE: ", mse)
print("RMSE: ", rmse)
print("MAE: ", mae)
print("R-squared: ", r2)

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00242/ENB2012_data.xlsx'
df = pd.read_excel(url)
df.columns = ['Relative_Compactness', 'Surface_Area', 'Wall_Area', 'Roof_Area', 'Overall_Height',
              'Orientation', 'Glazing_Area', 'Glazing_Area_Distribution', 'Heating_Load', 'Cooling_Load']

# Drop Cooling_Load from the dataframe
df.drop(['Cooling_Load'], axis=1, inplace=True)



# Split the dataset into training and testing sets
train_data, test_data, train_target, test_target = train_test_split(df.iloc[:, :-1], df.iloc[:, -1],
                                                                    test_size=0.3, random_state=50)


from sklearn.tree import DecisionTreeRegressor

# Define the hyperparameter search space for the decision tree model
search_space = {
     'max_depth': (1, 50),
    'min_samples_split': (2, 10),
    'min_samples_leaf': (1, 10),
    'max_features': (1, 9)
}

dt = DecisionTreeRegressor(random_state=50)

opt = BayesSearchCV(
    dt,
    search_space,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    cv=5,
    n_iter=50,
    verbose=0,
    random_state=50,
    return_train_score=True
)

opt.fit(train_data, train_target)

print('Best hyperparameters:', opt.best_params_)

import numpy as np
# Evaluate the decision tree model on the testing data using the best hyperparameters found
dt_best = DecisionTreeRegressor(random_state=0, **opt.best_params_)
dt_best.fit(train_data, train_target)
dt_preds = dt_best.predict(test_data)
dt_mse = mean_squared_error(test_target, dt_preds)
dt_rmse = np.sqrt(dt_mse)
dt_r2 = r2_score(test_target, dt_preds)
dt_mae = mean_absolute_error(test_target, dt_preds)


# Evaluate the decision tree model on the train data using the best hyperparameters founddt_preds2 = dt_best.predict(train_data)
dt_preds2 = dt_best.predict(train_data)
dt_mse2 = mean_squared_error(train_target, dt_preds2)
dt_rmse2 = np.sqrt(dt_mse2)
dt_r2_train = r2_score(train_target, dt_preds2)
dt_mae2 = mean_absolute_error(train_target, dt_preds2)

# Print the evaluation metrics for the decision tree model
print('Decision Tree - Test MSE: {:.4f}'.format(dt_mse))
print('Decision Tree - Test RMSE: {:.4f}'.format(dt_rmse))
print('Decision Tree - Test R^2: {:.4f}'.format(dt_r2))
print('Decision Tree - Train MSE: {:.4f}'.format(dt_mse2))
print('Decision Tree - Train RMSE: {:.4f}'.format(dt_rmse2))
print('Decision Tree - Train R^2: {:.4f}'.format(dt_r2_train))
print('Decision Tree - Test MAE: {:.4f}'.format(dt_mae))
print('Decision Tree - Train MAE: {:.4f}'.format(dt_mae2))

from sklearn.ensemble import StackingRegressor
rf_model = RandomForestRegressor()
estimators =[('xgb',rf_model),('rf',rf_model)]
#estimators =[('xgb',xgb_model),('rf',rf_model),('dtree',dt)]

stack_reg = StackingRegressor(estimators=estimators, final_estimator=dt)
stack_reg.fit(train_data, train_target)

#Prediction of Stack train and Stack Test data
stack_preds_test =  stack_reg.predict(test_data)
stack_preds_train = stack_reg.predict(train_data)

#Calculating MSE and RMSE of stacked training and testing
stack_mse_test = mean_squared_error(test_target,stack_preds_test)
stack_rmse_test = np.sqrt(stack_mse_test)

stack_mse_train = mean_squared_error(train_target,stack_preds_train)
stack_rmse_train = np.sqrt(stack_mse_train)

#Calculating MAE of stacked training and testing
stack_mae_test = mean_absolute_error(test_target,stack_preds_test)
stack_mae_train = mean_absolute_error(train_target,stack_preds_train)

#Calculating R^2 of stacked training and testing
stack_r2_test = r2_score(test_target,stack_preds_test)
stack_r2_train = r2_score(train_target,stack_preds_train)

#Printing Evaluation Matrix for Stacked Training and Test data
print('Stacked Test MSE: {:.4f}'.format(stack_mse_test))
print('Stacked Test RMSE: {:.4f}'.format(stack_rmse_test))
print('Stacked Train MSE: {:.4f}'.format(stack_mse_train))
print('Stacked Train RMSE: {:.4f}'.format(stack_rmse_train))
print('Stacked Test MAE: {:.4f}'.format(stack_mae_test))
print('Stacked Train MAE: {:.4f}'.format(stack_mae_train))
print('Stacked Test R^2: {:.4f}'.format(stack_r2_test))
print('Stacked Train R^2: {:.4f}'.format(stack_r2_train))





