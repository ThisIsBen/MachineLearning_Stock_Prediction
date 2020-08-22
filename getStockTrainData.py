# coding: utf-8

import requests
import json
import csv
import time, datetime,os,shutil
from bs4 import BeautifulSoup
import pandas



##########Parameter area
#id_list = ['2303','2330','1234','3006','2412'] #inout the stock IDs
id_list = ['2317','2330','2885'] 

now = datetime.datetime.now()
#/#
thisYear=2016
#/#
#year_list = range (2007,now.year+1) #since 2007 to this year
#year_list = range (thisYear,now.year+1) #since 2007 to this year
year_list = range (thisYear,now.year+1) #get 2016 data


#/#
#Use Taiwan year to retrieve 3 major juristic person data
#juristicYear_list = range ((thisYear-1911),(now.year+1)-1911) #since 2007 to this year
juristicYear_list = range ((thisYear-1911),(now.year)-1911) #get 2016 data



#use the past 3 days' data to predict next day's stock
feature_days=3

#/#
month_list = range(1,13)  # 12 months
#month_list = range(1,11)  # 1-10 month


##########Parameter area






#standard web crawing process
def get_webmsg (year, stock_id):
    firstMonth=True
    accumulate_dict = {}
    for month in month_list:
        date = str (year) + "{0:0=2d}".format(month) +'01' ## format is yyyymmdd
        sid = str(stock_id)
        url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+sid
        res =requests.post(url_twse,)
        soup = BeautifulSoup(res.text , 'html.parser')
        #print(soup.text)
        smt = json.loads(soup.text)     #convert data into json
        #print(smt)
        if(firstMonth):
            accumulate_dict.update(smt)
            firstMonth=False
        #print(accumulate_dict)
        else:
            accumulate_dict['data'].extend(smt['data'])
    
    
    return accumulate_dict




def write_csv(stock_id,directory,filename,smt) :
    writefile = directory + filename               #set output file name
    outputFile = open(writefile,'w',newline='')
    outputWriter = csv.writer(outputFile)
    '''
    head = ''.join(smt['title'].split())
    a = [head,""]
    outputWriter.writerow(a)
    '''
    outputWriter.writerow(smt['fields'])
    for data in (smt['data']):
        outputWriter.writerow(data)

    outputFile.close()




#create a directory in the current one doesn't exist
def makedirs (year, stock_id):
    sid = str(stock_id)
    yy      = str(year)
   
    directory = './ParsedStock'+'/'+sid +'/'+ yy+'StockData'
    
    
    #How to check existence of a folder and then remove it?
    if os.path.exists(directory):
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        #os.remove(directory)
    
    if not os.path.isdir(directory):
        os.makedirs (directory)  # os.makedirs able to create multi folders




def getStockData():

    for stock_id in id_list:
        for year in year_list:
            #for month in month_list:
                #if (dt.year == year and month > dt.month) :break  # break loop while month over current month
                #if (dt.year == year ) :break  # break loop while month over current month
                sid = str(stock_id)
                yy  = str(year)
                #mm  = month
                directory = './ParsedStock'+'/'+sid +'/'+yy +'StockData/'       #setting directory
                filename = str(yy)+'.csv'          #setting file name
                accumulate_dict = get_webmsg(year , stock_id)           #put the data into smt 
                #print(accumulate_dict)
                makedirs (year, stock_id)                  #create directory function
                write_csv (stock_id,directory, filename, accumulate_dict)    # write files into CSV
                time.sleep(1)
            


            
            














def setFeatureData(stock_id):
   
        #set up empty pandas dataframe as container
        accumulateJuristic = pandas.DataFrame()
        
        #set up empty pandas dataframe as container for trading volume
        tradingVolume = pandas.DataFrame()
        for year in juristicYear_list:
            ADYear=str(year+1911)
            for month in month_list:

                url= 'https://stock.wearn.com/netbuy.asp?Year='+str(year)+'&month='+"{0:0=2d}".format(month)+'&kind='+str(stock_id)
                #print(url)
                dfs=pandas.read_html(url)
                juristicPerson=dfs[0]

                juristicPerson=juristicPerson.iloc[:,1:]
                juristicPerson=juristicPerson.drop(juristicPerson.index[[0,1]])
                juristicPerson = juristicPerson.iloc[::-1]







                accumulateJuristic=pandas.concat([accumulateJuristic, juristicPerson])
            accumulateJuristic.columns=[u'投信',u'自營商',u'外資']
            accumulateJuristic=accumulateJuristic.reset_index(drop=True)
            '''
            if(stock_id=='2885'):
                firstMonth=True
                accumulate_dict = {}
                
                #parse trading volume for stock trading company
                for month in month_list:
                    
                    date = str (ADYear) + "{0:0=2d}".format(month) +'01' ## format is yyyymmdd
                    url_tradingVolume= 'http://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date='+date
                    #print(url)
                    
                    res =requests.post(url_tradingVolume,)
                    soup = BeautifulSoup(res.text , 'html.parser')
                    smt = json.loads(soup.text)     #convert data into json
                    
                    print(smt)
                    #dfs=pandas.read_html(url)
                    if(firstMonth):
                        accumulate_dict.update(smt)
                        firstMonth=False
                    #print(accumulate_dict)
                    else:
                        accumulate_dict['data'].extend(smt['data'][])

    
                   
                    juristicPerson=dfs[0]

                    juristicPerson=juristicPerson.iloc[:,1:]
                    juristicPerson=juristicPerson.drop(juristicPerson.index[[0,1]])
                    juristicPerson = juristicPerson.iloc[::-1]

                    #trim needless features
                    juristicPerson=juristicPerson.iloc[:,2:4]







                    tradingVolume=pandas.concat([tradingVolume, juristicPerson])
                tradingVolume.columns=[u'成交金額',u'成交筆數']
                tradingVolume=tradingVolume.reset_index(drop=True)
               '''

            
            
            
            
            # read stock data of the current iterated company 
            stockDataFilePath='./ParsedStock/'+str(stock_id)+'/'+ADYear+'StockData/'+ADYear+'.csv'
            #while not os.path.exists(stockDataFilePath):
            #    time.sleep(1)

            if os.path.isfile(stockDataFilePath):
                # read stock data of the current iterated company 
                stockData = pandas.read_csv(stockDataFilePath)

                stockData=stockData.iloc[:,2:9]
                
                #use the code below instead, if you want to view the date of each datum
                #stockData=stockData.iloc[:,0:8]

                featureData = pandas.concat([stockData,accumulateJuristic ], axis=1)
                #store to training data csv
                '''
                #add trading volume
                if(stock_id=='2885'):
                    featureData = pandas.concat([featureData,tradingVolume ], axis=1)
                '''
                #without column name
                #trainingData.to_csv('bin/ParsedStock/'+str(stock_id)+'_trainingData.csv', index=False,header=False)
                featureData.to_csv('./ParsedStock/TrainingDataSet/'+str(stock_id)+'_featureData.csv', index=False)

            else:
                raise ValueError("%s isn't a file!" % './ParsedStock/TrainingDataSet/'+str(stock_id)+'/'+ADYear+'StockData/'+ADYear+'.csv')
        
        #send featureData back to main function
        return featureData                
          
       
    
#write pandas dataframe to csv file               
def writeTrainingDataSet2Csv(DataFrame,stock_id,ClfOrRg):
    #store training data set to csv
    DataFrame.to_csv('./ParsedStock/TrainingDataSet/'+str(stock_id)+'_'+ClfOrRg+'_trainingDataSet.csv', index=False)

    
    
def setupTrainingDataSetFormat(trainingData):
    
    
    
    #get the number of records in trainingData
    numberOfRows=trainingData.shape[0]
    
    #create empty pandas dataframe as a container for classifier, rise regressor, and fall regressor usage
    clfTrainingDataSet = pandas.DataFrame()
    rgRiseTrainingDataSet = pandas.DataFrame()
    rgFallTrainingDataSet = pandas.DataFrame()
    
  
    #setup features and label them with the data of the past 3 days
    for row_index in range(0, numberOfRows-feature_days):
        
        #to generate column names e.g.,n天前開盤價
        daysBefore=feature_days
        
        
        #get the stock data of the previous 3 days and reset their index to merge them in the same row in later merge process.
        #由上而下 順序為 久到近
        #if(df_previousDay1.loc[0,'收盤價']=='--'):
        daysBefore=str(daysBefore) 
        df_previousDay1 = trainingData.iloc[[row_index]]       
        df_previousDay1=df_previousDay1.reset_index(drop=True)
        
        #/#with 成交量      
        #df_previousDay1.columns = [daysBefore+u'天前成交金額',daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前成交筆數',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']      
          
         #/#without 成交量      
        df_previousDay1.columns = [daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']

        daysBefore=int(daysBefore)
        daysBefore-=1
        daysBefore=str(daysBefore)
        df_previousDay2 = trainingData.iloc[[row_index+1]]
        df_previousDay2=df_previousDay2.reset_index(drop=True)
        
        #/# with 成交量 
        #df_previousDay2.columns = [daysBefore+u'天前成交金額',daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前成交筆數',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']
         
        #/#without 成交量      
        df_previousDay2.columns = [daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']
        
        
        daysBefore=int(daysBefore)
        daysBefore-=1
        daysBefore=str(daysBefore)
        df_previousDay3 = trainingData.iloc[[row_index+2]]
        df_previousDay3=df_previousDay3.reset_index(drop=True) 
        
        #/# with 成交量 
        #df_previousDay3.columns = [daysBefore+u'天前成交金額',daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前成交筆數',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']        
         
         #/#without 成交量 
        df_previousDay3.columns = [daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']
        
        ######code modification area
        # if more past days' data is required, add more  df_previousDay3 = pd.DataFrame(trainingData.iloc[row_index+n]) below 
        ######code modification area
        
        
        
        aRecordOfTrainingData=pandas.concat([df_previousDay1,df_previousDay2,df_previousDay3], axis=1)
   
        
        #label the current training data record
        
        #the default value of BoomOrBust is set to 0,which means Bust
        aRecordOfTrainingData['RiseOrFall']=0
        
        #avoid strange str that can't be converted to float
        if(trainingData.loc[row_index+feature_days,'漲跌價差']=='X0.00'):
            trainingData.loc[row_index+feature_days,'漲跌價差']='0'
        
        
        #label 1 if it's Boom
        if(float(trainingData.loc[row_index+feature_days,'漲跌價差'])>0 ):
            aRecordOfTrainingData['RiseOrFall']=1

        #add a record of feature and label to clf trainingDataSet  
        clfTrainingDataSet=pandas.concat([clfTrainingDataSet, aRecordOfTrainingData])
        
        
       
        #label the value with Price Fluctuation Limit.
        priceFluctuationLimit=float(trainingData.loc[row_index+feature_days,'漲跌價差'])
        aRecordOfTrainingData['RiseOrFall']=priceFluctuationLimit
        
        
        
        #if the Price Fluctuation Limit is positive, put this feature record to rise regressor training data set 
        if (priceFluctuationLimit>0 ):
            
            #add a record of feature and label to rg trainingDataSet  
            rgRiseTrainingDataSet=pandas.concat([rgRiseTrainingDataSet, aRecordOfTrainingData])
        
        #if the Price Fluctuation Limit is negative, put this feature record to fall regressor training data set
        elif (priceFluctuationLimit<=0 ):
            #add a record of feature and label to rg trainingDataSet  
            rgFallTrainingDataSet=pandas.concat([rgFallTrainingDataSet, aRecordOfTrainingData])
        
    
    return clfTrainingDataSet,rgRiseTrainingDataSet,rgFallTrainingDataSet

def main():
    
    #/#get stock data and store it as csv 
    #getStockData()
    
    for stock_id in id_list:
        #/#setup all the features
        #featureData=setFeatureData(stock_id)
       
        
        featureData=pandas.read_csv('./ParsedStock/TrainingDataSet/'+str(stock_id)+'_featureData.csv') #2017 only
        #setup training data set
        
      
        clfTrainingDataSet,rgRiseTrainingDataSet,rgFallTrainingDataSet=setupTrainingDataSetFormat(featureData)

        #write pandas dataframe to csv file for clf usage 
        writeTrainingDataSet2Csv(clfTrainingDataSet,stock_id,'classifier')
        
        #write pandas dataframe to csv file for rise rg usage
        writeTrainingDataSet2Csv(rgRiseTrainingDataSet,stock_id,'riseRegressor')
        
        
         #write pandas dataframe to csv file for fall rg usage
        writeTrainingDataSet2Csv(rgFallTrainingDataSet,stock_id,'fallRegressor')
       
    
    
    
    
if __name__ == "__main__":
    main()
