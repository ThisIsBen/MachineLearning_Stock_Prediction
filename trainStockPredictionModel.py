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
######parameter area
feature_days=3
current_features_per_day=8
totalFeatureForOneRecord=feature_days*current_features_per_day
id_list = ['2317','2330'] 


######parameter area


#######
#gather all the training data of the company listed in stock_id to train the model
#######

def train_RF_CLF_Model(stock_id):
    #header = ['開盤價','最高價','最低價','收盤價','漲跌價差','投信','自營商','外資']

    trainingDataFilePath='./ParsedStock/TrainingDataSet/'+str(stock_id)+'_classifier_trainingDataSet.csv'
    #train the stock prediction model
    #load historical stock training data
    trainingDataframe = pandas.read_csv(trainingDataFilePath)
    trainingArray = trainingDataframe.values
    X = trainingArray[:,0:totalFeatureForOneRecord]
    Y = trainingArray[:,totalFeatureForOneRecord]
    test_size = 0.33
    seed = 2

    #Split arrays or matrices into random train and test subsets
    stock_train_X, stock_test_X, stock_train_Y, stock_test_Y = train_test_split(X, Y, test_size=test_size, random_state=seed)
    print("x of training data: {}".format( stock_train_X[:2]))
    print("Y of training data: {}".format( stock_train_Y[:2]))




    #stock_train_X = np.load('train_X.npy') # train 2017-05-01 ~ 2017-05-31
    #stock_train_Y = np.load('train_Y.npy')
    #stock_test_X = np.load('test_X.npy') # test 2017-06-01 ~ 2017-06-30
    #stock_test_Y = np.load('test_Y.npy')

    #print("Y of training data: {}".format( stock_train_Y[:5]))
    #print("X of training data: {}".format( stock_train_X[:3]))

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
    model = gs.best_estimator_

    # Save model
    f = open('./'+str(stock_id)+'_RF_Clf_model.pkl', "wb")
    pickle.dump(model, f)





def main():
    
    
    #train and output a model for each stock_id
    for stock_id in id_list:
        train_RF_CLF_Model(stock_id)
            
            
    
    
if __name__ == "__main__":
    main()


