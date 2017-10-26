#randomforest classifier

import numpy as np
import sklearn
#import matplotlib.pyplot as plt
## Split data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold,cross_val_predict
import pickle
from sklearn.decomposition import PCA
import pandas
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
######parameter area
feature_days=3
current_features_per_day=8
totalFeatureForOneRecord=feature_days*current_features_per_day
id_list = ['2317','2330'] 

Rise_Linear_RG_Model_Polynomial_Features_degree=1
Fall_Linear_RG_Model_Polynomial_Features_degree=1
######parameter area


#######
#gather all the training data of the company listed in stock_id to train the model
#######


    



def train_RF_CLF_Model(stock_id):
    #header = ['開盤價','最高價','最低價','收盤價','漲跌價差','投信','自營商','外資']
    
    #load CLF TrainingDataSet according to stock_id
    trainingDataFilePath='./ParsedStock/TrainingDataSet/'+str(stock_id)+'_classifier_trainingDataSet.csv'
    #train the stock prediction model
    #load historical stock training data
    trainingDataframe = pandas.read_csv(trainingDataFilePath)
    trainingArray = trainingDataframe.values
    X = trainingArray[:,0:totalFeatureForOneRecord]
    Y = trainingArray[:,totalFeatureForOneRecord]
    test_size = 0.33
    seed = 2
    
    stock_train_X=X
    stock_train_Y=Y
    #Split arrays or matrices into random train and test subsets
    #stock_train_X, stock_test_X, stock_train_Y, stock_test_Y = train_test_split(X, Y, test_size=test_size, random_state=seed)
    #print("x of training data: {}".format( stock_train_X[:2]))
    #print("Y of training data: {}".format( stock_train_Y[:2]))
    
    



    #stock_train_X = np.load('train_X.npy') # train 2017-05-01 ~ 2017-05-31
    #stock_train_Y = np.load('train_Y.npy')
    #stock_test_X = np.load('test_X.npy') # test 2017-06-01 ~ 2017-06-30
    #stock_test_Y = np.load('test_Y.npy')

   
    ###training
    inner_cv = KFold(n_splits=5, shuffle=True, random_state=5)
    #outer_cv = KFold(n_splits=5, shuffle=True, random_state=5)


    #Use randomforest classifier  : 

    #use pipeline
    #10/16
    #select = sklearn.feature_selection.SelectKBest(k=30)
    #clf = Pipeline([ ('featureSelection', select),('randomForest', RandomForestClassifier(n_estimators=100))])
    clf = Pipeline([ ('scl', StandardScaler()),
                    ('pca', PCA(n_components=2)),('randomForest', RandomForestClassifier(n_estimators=100))])

    #C and gamma are randomforest classifier's parameters       
    parameters = { 'randomForest__n_estimators': [100, 200, 700],
        'randomForest__max_features': [ 'sqrt', 'log2']}


    #Tuning hyperparameters via grid search
    gs = GridSearchCV(estimator=clf, 
                      param_grid=parameters, 
                      scoring='accuracy', 
                      cv=inner_cv,
                     )



    # Non_nested parameter search and scoring
    gs = gs.fit(stock_train_X, stock_train_Y)

    print('the best score of trainaing data: {}'.format(gs.best_score_))
    print('the best parameters of  trainaing data: {}'.format(gs.best_params_))

    # Nested CV with parameter optimization
    #nested_score = cross_val_score(gs, X=stock_train_X, y=stock_train_Y, cv=outer_cv)
    #print('the best score of nested CV of training data: {}'.format(nested_score.mean()))



    #put the retrieved best estimator to the test
    CLFmodel = gs.best_estimator_

    # Save model
    f = open('./TrainedModel/'+str(stock_id)+'_RF_Clf_model.pkl', "wb")
    pickle.dump(CLFmodel, f)

#use SVR for rise RG
def train_Rise_Linear_RG_Model(stock_id):
    #load rise RG TrainingDataSet according to stock_id
    trainingDataFilePath='./ParsedStock/TrainingDataSet/'+str(stock_id)+'_riseRegressor_trainingDataSet.csv'
    
    #train the stock prediction model
    #load historical stock training data
    trainingDataframe = pandas.read_csv(trainingDataFilePath)
    trainingArray = trainingDataframe.values
    X = trainingArray[:,0:totalFeatureForOneRecord]
    Y = trainingArray[:,totalFeatureForOneRecord]
    test_size = 0.33
    seed = 2

    stock_train_X=X
    stock_train_Y=Y
    #Split arrays or matrices into random train and test subsets
    #stock_train_X, stock_test_X, stock_train_Y, stock_test_Y = train_test_split(X, Y, test_size=test_size, random_state=seed)
    
    inner_cv = KFold(n_splits=5, shuffle=True, random_state=5)
    '''
    polynomial_features = PolynomialFeatures(degree=Rise_Linear_RG_Model_Polynomial_Features_degree,
                                             include_bias=False)
    linear_regression = LinearRegression()
    pipeline = Pipeline([('scl', StandardScaler()),
                ('pca', PCA(n_components=2)),("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])
 
    #defaults are: True,False,True respectively
    parameters = {'linear_regression__fit_intercept':[True,False], 'linear_regression__normalize':[True,False], 'linear_regression__copy_X':[True, False]}
    gs = GridSearchCV(estimator=pipeline,param_grid=parameters, cv=inner_cv)
    '''
    parameters = {'SVR_RG__kernel':['linear', 'rbf','poly'], 'SVR_RG__C': [0.01, 0.06, 3], 'SVR_RG__gamma': [0.1, 0.3, 'auto'],'SVR_RG__degree':[2,4]}
    clf = Pipeline([('scl', StandardScaler()),('pca', PCA(n_components=2)), ('SVR_RG', SVR())])
    gs = GridSearchCV(estimator=clf, 
                  param_grid=parameters, 
                  cv=inner_cv,
                  n_jobs=-1)
   
    gs=gs.fit(stock_train_X, stock_train_Y)
    

    print( "Grid best : {}".format( gs.best_score_))
    print('the best parameters of  trainaing data: {}'.format(gs.best_params_))
    print('Rise_Linear_RG_Model_Polynomial_Features_degree: {}'.format(Rise_Linear_RG_Model_Polynomial_Features_degree))
    
    
    #put the retrieved best estimator to the test
    riseRGmodel = gs.best_estimator_

    # Save model
    f = open('./TrainedModel/'+str(stock_id)+'_Rise_LIN_RG_model.pkl', "wb")
    pickle.dump(riseRGmodel, f)
    
#use linear RG for fall RG
def  train_Fall_Linear_RG_Model(stock_id):
    #load rise RG TrainingDataSet according to stock_id
    trainingDataFilePath='./ParsedStock/TrainingDataSet/'+str(stock_id)+'_fallRegressor_trainingDataSet.csv'
   
    #train the stock prediction model
    #load historical stock training data
    trainingDataframe = pandas.read_csv(trainingDataFilePath)
    trainingArray = trainingDataframe.values
    X = trainingArray[:,0:totalFeatureForOneRecord]
    Y = trainingArray[:,totalFeatureForOneRecord]
    test_size = 0.33
    seed = 2
    
    stock_train_X=X
    stock_train_Y=Y
    #Split arrays or matrices into random train and test subsets
    #stock_train_X, stock_test_X, stock_train_Y, stock_test_Y = train_test_split(X, Y, test_size=test_size, random_state=seed)
    
    inner_cv = KFold(n_splits=5, shuffle=True, random_state=5)
    
    polynomial_features = PolynomialFeatures(degree=Fall_Linear_RG_Model_Polynomial_Features_degree,
                                             include_bias=False)
    linear_regression = LinearRegression()
    pipeline = Pipeline([('scl', StandardScaler()),
                ('pca', PCA(n_components=2)),("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])
    
    #defaults are: True,False,True respectively
    parameters = {'linear_regression__fit_intercept':[True,False], 'linear_regression__normalize':[True,False], 'linear_regression__copy_X':[True, False]}
    gs = GridSearchCV(estimator=pipeline,param_grid=parameters, cv=inner_cv)
   
   
    gs=gs.fit(stock_train_X, stock_train_Y)
    

    print( "Grid best : {}".format( gs.best_score_))
    print('the best parameters of  trainaing data: {}'.format(gs.best_params_))
    print('Fall_Linear_RG_Model_Polynomial_Features_degree: {}'.format(Rise_Linear_RG_Model_Polynomial_Features_degree))
    
    
    #put the retrieved best estimator to the test
    fallRGmodel = gs.best_estimator_

    # Save model
    f = open('./TrainedModel/'+str(stock_id)+'_Fall_LIN_RG_model.pkl', "wb")
    pickle.dump(fallRGmodel, f)
   
def main():
    
    
    #train and output a model for each stock_id
    for stock_id in id_list:
        
        #train clf model
        train_RF_CLF_Model(stock_id)
        
        #train rise rg model
        train_Rise_Linear_RG_Model(stock_id)
        
        #train fall rg model
        train_Fall_Linear_RG_Model(stock_id)
            
    
    
if __name__ == "__main__":
    main()


