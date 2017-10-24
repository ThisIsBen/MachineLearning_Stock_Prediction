import numpy as np
import sklearn
#import matplotlib.pyplot as plt
## Split data
import pickle
import pandas
import sys

#####parameter area

#stock_id that will be predicted
id_list = ['2317','2330'] 

#####parameter area







#####testing
def predict_with_RF_CLF(todayDate,stock_id):
    
    
    
    #load today's feature day to predict today's stock rise or fall
    testingDataFilePath='./ParsedStock/TestingDataSet/'+str(stock_id)+'_testingDataSet/'+todayDate+'.csv'
    testingDataframe = pandas.read_csv(testingDataFilePath)
    testingDataSet= testingDataframe.values
    print("testingDataSet data of today\'s "+stock_id+": {}".format( testingDataSet))
    
    
    # load the corresponding RF_CLF model
    f = open('./'+str(stock_id)+'_RF_Clf_model.pkl', 'rb')
    RF_CLF_ReloadModel = pickle.load(f)

    #use the testing data set to predict today's stock rise or fall
    testingDataSet_y_riseOrFall_pred = RF_CLF_ReloadModel.predict(testingDataSet)
    print (' RF_CLF Prediction of today\'s '+stock_id+' testing data set: {}'.format(testingDataSet_y_riseOrFall_pred))

def main():
    
    
    if(sys.argv[1]==sys.argv[2]):
        for stock_id in id_list:
            todayDate=sys.argv[1]
            predict_with_RF_CLF(todayDate,stock_id)
    
    
if __name__ == "__main__":
    main()
