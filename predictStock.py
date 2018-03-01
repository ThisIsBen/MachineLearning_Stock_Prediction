import numpy as np
import sklearn
#import matplotlib.pyplot as plt
## Split data
import pickle
import pandas
import sys
import json
import os
from decimal import Decimal, getcontext
#####parameter area

#stock_id that will be predicted
id_list = ['2317','2330'] 
#id_list = ['2330','2885'] 
weight=int(4/len(id_list))
life=3

#make LIBSVM model switchable
dict_LIBSVM_Model={'noTradVol':'CLF_Train.scale.model','withTradVol':'CLF_TrainTradVol.scale.model'}
#create a dict to store 停利點 for each company:
#stopLossPointDict= {'2330_riseStopLossPoint': 1, '2330_fallStopLossPoint': -0.5, '2317_riseStopLossPoint':0.5,'2317_fallStopLossPoint': -0.5}

dict_stop_loss_point={'2330':0.5,'2317':0.5,'2885':0.05}
#####parameter area



def loadTestingDataSet(todayDate,stock_id):
    #load today's feature day to predict today's stock rise or fall
    testingDataFilePath='./ParsedStock/TestingDataSet/'+str(stock_id)+'_testingDataSet/'+todayDate+'.csv'
    testingDataframe = pandas.read_csv(testingDataFilePath)
    testingDataSet= testingDataframe.values
    print("testingDataSet data of today\'s "+stock_id+": {}".format( testingDataSet))
    
    return testingDataSet,testingDataframe



#####testing
def predict_with_RF_CLF(testingDataSet,stock_id):

    # load the corresponding RF_CLF model
    f = open('./TrainedModel/'+str(stock_id)+'_RF_Clf_model.pkl', 'rb')
    RF_CLF_ReloadModel = pickle.load(f)

    #use the testing data set to predict today's stock rise or fall
    testingDataSet_y_riseOrFall_pred = RF_CLF_ReloadModel.predict(testingDataSet)
    print (' RF_CLF Prediction of today\'s '+stock_id+' testing data set: {}'.format(testingDataSet_y_riseOrFall_pred))

    return testingDataSet_y_riseOrFall_pred[0]

#get LIBSVM result
def predict_with_LIBSVM(startDate,stock_id):

   
    #scale LIBSVM testing data
    os.system("svm-scale -r scale ParsedStock/TestingDataSet/LIBSVM"+stock_id+"_testingDataSet/"+stock_id+"_"+startDate+".csv > LIBSVMTestResult/"+stock_id+"_"+startDate+"Test.scale")
    
    #ParsedStock/TestingDataSet/LIBSVM2317_testingDataSet/2317_2017-11-1.csv
    
    
 
    #predict LIBSVM testing data
    os.system("svm-predict LIBSVMTestResult/"+stock_id+"_"+startDate+"Test.scale TrainedModel/LIBSVM_Model/LIBSVM"+stock_id+dict_LIBSVM_Model['withTradVol']+" LIBSVMTestResult/"+stock_id+"_LIBSVMResult/"+stock_id+"_"+startDate+"TestResult.txt")
    
    #read in the LIBSVM prediction result
    with open("LIBSVMTestResult/"+stock_id+"_LIBSVMResult/"+stock_id+"_"+startDate+"TestResult.txt") as f:
        LIBSVMPredictResult = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    LIBSVMPredictResult = [x.strip() for x in LIBSVMPredictResult]
    
    #return the LIBSVM prediction result of the input startDate
    return int(LIBSVMPredictResult[0])
    
    '''
    # load the corresponding RF_CLF model
    f = open('./TrainedModel/'+str(stock_id)+'_RF_Clf_model.pkl', 'rb')
    RF_CLF_ReloadModel = pickle.load(f)

    #use the testing data set to predict today's stock rise or fall
    testingDataSet_y_riseOrFall_pred = RF_CLF_ReloadModel.predict(testingDataSet)
    print (' RF_CLF Prediction of today\'s '+stock_id+' testing data set: {}'.format(testingDataSet_y_riseOrFall_pred))

    return testingDataSet_y_riseOrFall_pred[0]
    '''

def predicti_rise_extent_with_LIN_RG(testingDataSet,stock_id):


    # load the corresponding RF_CLF model
    f = open('./TrainedModel/'+str(stock_id)+'_Rise_LIN_RG_model.pkl', 'rb')
    Rise_SVR_RG_ReloadModel = pickle.load(f)

    #use the testing data set to predict today's stock rise or fall
    riseChangeExtent = Rise_SVR_RG_ReloadModel.predict(testingDataSet)
    print (' Rise_LIN_RG change extent Prediction of today\'s '+stock_id+' testing data set: {}'.format(riseChangeExtent))


    return riseChangeExtent[0]


def predicti_fall_extent_with_LIN_RG(testingDataSet,stock_id):


    # load the corresponding RF_CLF model
    f = open('./TrainedModel/'+str(stock_id)+'_Fall_LIN_RG_model.pkl', 'rb')
    Fall_LIN_RG_ReloadModel = pickle.load(f)

    #use the testing data set to predict today's stock rise or fall
    fallChangeExtent = Fall_LIN_RG_ReloadModel.predict(testingDataSet)
    print (' Fall_LIN_RG change extent Prediction of today\'s '+stock_id+' testing data set: {}'.format(fallChangeExtent))


    return fallChangeExtent[0]



###output decision file to commit folder
def outputDecisionFile(list_overallStockPredictionResult,startDate,endDate):
    print('Decision file content: {}'.format(list_overallStockPredictionResult))
    with open('../commit/'+startDate+'_'+endDate+'.json', 'w') as f:
        json.dump(list_overallStockPredictionResult, f, indent=4)





def main():
    
    


    
    if(sys.argv[1]==sys.argv[2]):

        #declare a list to store the content of each company's prediction result
        list_overallStockPredictionResult=[]
        
        #create a dict to contain the data required in decision file for each company.
        dict_eachCompanyStockPrediction={}
        
        #get the input start and end date
        startDate=sys.argv[1]
        endDate=sys.argv[2]

        for stock_id in id_list:
            
            #load testing data set
            testingDataSet,testingDataframe=loadTestingDataSet(startDate,stock_id)

            
            ###############SKLearn VS LIBSVM
            #predict rise or fall with clf
            #riseOrFall=predict_with_RF_CLF(testingDataSet,stock_id)
            
            
            
            #predict rise or fall with LIBSVM
            riseOrFall=predict_with_LIBSVM(startDate,stock_id)
            
            ################SKLearn VS LIBSVM
            

            print(riseOrFall)
        
        
        
        
            ###set stock code of the current company
            dict_eachCompanyStockPrediction['code']=str(stock_id)
           
            ###set weight=4/len(id_list)
            dict_eachCompanyStockPrediction['weight']=weight


            ###set life=3
            dict_eachCompanyStockPrediction['life']=life

            #get previous Day Close Price from testing panda Dataframe
            previousDayClosePrice=testingDataframe.loc[0,'1天前收盤價']
            
            ###set open_price=前日收盤價 (read form testingDataSet csv file, and add new keys to a dict)
            dict_eachCompanyStockPrediction['open_price']=previousDayClosePrice
           
            

           

            #if it will rise tomorrow, try to predict how much it will rise.
            if(riseOrFall==1):
                ###set type to 'buy'
                dict_eachCompanyStockPrediction['type']='buy'




                riseChangeExtent=predicti_rise_extent_with_LIN_RG(testingDataSet,stock_id)
                
                ###set close_high_price=前日收盤價+riseChangeExtent
                dict_eachCompanyStockPrediction['close_high_price']=previousDayClosePrice+riseChangeExtent
                
                



                #displayed precision 
                getcontext().prec = 5
                
                
                 ###set close_low_price = 前日收盤價+(-0.5)
                dict_eachCompanyStockPrediction['close_low_price']=float(Decimal(previousDayClosePrice)-Decimal(dict_stop_loss_point[stock_id]))
                                                                         


                #planB
                #set close_low_price = 前日收盤價+[stock_id]fallStopLossPoint




            #if it will fall tomorrow, try to predict how much it will fall.
            elif(riseOrFall==0):

                ###set type to 'short'
                dict_eachCompanyStockPrediction['type']='short'



                fallChangeExtent=predicti_fall_extent_with_LIN_RG(testingDataSet,stock_id)
                
                ###set close_low_price=前日收盤價+fallChangeExtent
                dict_eachCompanyStockPrediction['close_low_price']=previousDayClosePrice+fallChangeExtent
                



               
                    ###set close_high_price = 前日收盤價+0.5
                dict_eachCompanyStockPrediction['close_high_price']=float(Decimal(previousDayClosePrice)+                               Decimal(dict_stop_loss_point[stock_id]))

                #planB
                #set close_high_price = 前日收盤價+[stock_id]riseStopLossPoint


            


            #append the each company's prediction data to the overall stock prediction list
            list_overallStockPredictionResult.append(dict_eachCompanyStockPrediction.copy())

            #clear the content of the current company's prediction data to contain that of the next company.
            dict_eachCompanyStockPrediction.clear()



        #output decision file to commit folder
        outputDecisionFile(list_overallStockPredictionResult,startDate,endDate)








    
    
if __name__ == "__main__":
    main()
