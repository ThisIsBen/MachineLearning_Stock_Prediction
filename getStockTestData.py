# coding: utf-8

import requests
import json
import csv
import time,datetime,os,shutil
from bs4 import BeautifulSoup
import pandas as pd
import sys
from threading import Timer


######parameter area
#id_list = ['2303','2330','1234','3006','2412'] #inout the stock IDs
startYear=2020
now = datetime.datetime.now()
year_list = range (startYear,now.year+1)



#use the past 3 days' data to predict next day's stock
feature_days=5
    
#without 'RiseOrFall'

#/#with 成交量
#list_colName=[u'3天前成交金額',u'3天前開盤價',u'3天前最高價',u'3天前最低價',u'3天前收盤價',u'3天前漲跌價差',u'3天前成交筆數',u'3天前投信',u'3天前自營商',u'3天前外資',u'2天前成交金額',u'2天前開盤價',u'2天前最高價',u'2天前最低價',u'2天前收盤價',u'2天前漲跌價差',u'2天前成交筆數',u'2天前投信',u'2天前自營商',u'2天前外資',u'1天前成交金額',u'1天前開盤價',u'1天前最高價',u'1天前最低價',u'1天前收盤價',u'1天前漲跌價差',u'1天前成交筆數',u'1天前投信',u'1天前自營商',u'1天前外資']




#/#without 成交量

list_colName=[]
for daysBefore in range (feature_days,0,-1):
    daysBefore=str(daysBefore)
    list_colName.append(daysBefore+u'天前開盤指數')
    list_colName.append(daysBefore+u'天前最高指數')
    list_colName.append(daysBefore+u'天前最低指數')
    list_colName.append(daysBefore+u'天前收盤指數')
    list_colName.append(daysBefore+u'天前成交股數')
    list_colName.append(daysBefore+u'天前成交金額')
    list_colName.append(daysBefore+u'天前成交筆數')
    list_colName.append(daysBefore+u'天前漲跌點數')

######parameter area

#set this program be executed automatically at 17:00 every day
######set this program be executed at 17:00 the next day

x=datetime.datetime.today()
y=x.replace(day=x.day+1, hour=17, minute=0, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

######set this program be executed at 17:00 the next day






#standard web crawing process
def get_webmsg ( stock_id,thisYear,thisMonth):
    highLow_firstMonth=True
    volumne_firstMonth=True
    highLow_accumulate_dict = {}
    volumne_accumulate_dict = {}
   
    date = thisYear + "{0:0=2d}".format(thisMonth) +'01' ## format is yyyymmdd
    #get 發行量加權股價指數歷史資料
    url_twse = 'https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date='+date
    res =requests.post(url_twse,)
    soup = BeautifulSoup(res.text , 'html.parser')
    #print(soup.text)
    smt = json.loads(soup.text)     #convert data into json
    #print(smt)
    if(highLow_firstMonth):
        highLow_accumulate_dict.update(smt)
        highLow_firstMonth=False
    #print(accumulate_dict)
    else:
        highLow_accumulate_dict['data'].extend(smt['data'])
    
    
    #get 市場成交資訊
    url_twse = 'https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date='+date
    res =requests.post(url_twse,)
    soup = BeautifulSoup(res.text , 'html.parser')
    #print(soup.text)
    smt = json.loads(soup.text)     #convert data into json
    #print(smt)
    if(volumne_firstMonth):
        volumne_accumulate_dict.update(smt)
        volumne_firstMonth=False
    #print(accumulate_dict)
    else:
        volumne_accumulate_dict['data'].extend(smt['data'])
        
    return highLow_accumulate_dict, volumne_accumulate_dict




def write_csv(stock_id,directory,filename,highLow_accumulate_dict,volume_accumulate_dict,IsFirSecDay=False) :
    
    writefile = directory + filename
    df_stockHighLow = pd.DataFrame(highLow_accumulate_dict['data'], columns =highLow_accumulate_dict['fields']) #convert data from dict to pandas dataframe
    df_stockVolume = pd.DataFrame(volume_accumulate_dict['data'], columns =volume_accumulate_dict['fields'])  #convert data from dict to pandas dataframe
    
    
    df_stockHighLow = pd.DataFrame(highLow_accumulate_dict['data'], columns =highLow_accumulate_dict['fields']) #convert data from dict to pandas dataframe
    df_stockVolume = pd.DataFrame(volume_accumulate_dict['data'], columns =volume_accumulate_dict['fields'])  #convert data from dict to pandas dataframe
    
    
    df_stockHighLow=df_stockHighLow.drop('日期',axis=1)
    df_stockVolume=df_stockVolume.drop('日期',axis=1)
    df_stockVolume=df_stockVolume.drop('發行量加權股價指數',axis=1)
    #combine df_stockHighLow and df_stockVolume
    df_combinedStockData = pd.concat([df_stockHighLow, df_stockVolume], axis=1, sort=False)
    
    #if today is not the first or the second day on a month
    if(IsFirSecDay==False):
        #write header 
        df_combinedStockData.to_csv(writefile, index=False, encoding='utf-8')
        
        
    else:
        #do not write header
         df_combinedStockData.to_csv(writefile, index=False,header=None, encoding='utf-8')
  


#create a directory in the current one doesn't exist
def makedirs (stock_id):
    sid = str(stock_id)
   
   
    directory = './ParsedStock'+'/ParsedTestingData_'+sid 
    
    
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




def getStockData(thisYear,thisMonth,today):

    for stock_id in year_list:
        #for year in year_list:
            #for month in month_list:
                #if (dt.year == year and month > dt.month) :break  # break loop while month over current month
                #if (dt.year == year ) :break  # break loop while month over current month
                sid = str(stock_id)
                
                #mm  = month
                directory = './ParsedStock'+'/ParsedTestingData_'+sid +'/'       #setting directory
                filename = str(thisMonth)+'_'+today+'.csv'          #setting file name
                
                
                IsFirSecDay=True
                #if today is the first or the second day on a month
                if(today=='1' or today=='2'):
                    
                    #get the stock data from last month
                    lastMonth_highLow_accumulate_dict,lastMonth_volume_accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth-1)           #put the data into smt 
                    
                    makedirs (stock_id)                  #create directory function
                   
                    time.sleep(1)
                    
                    
                    #get the stock data of this month  
                    thisMonth_highLow_accumulate_dict,thisMonth_volume_accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth)           #put the data into smt 
                       
                    #combine the stock data of this month and last month
                    lastMonth_highLow_accumulate_dict['data'] = lastMonth_highLow_accumulate_dict['data']+thisMonth_highLow_accumulate_dict['data']
                    lastMonth_volume_accumulate_dict['data'] = lastMonth_volume_accumulate_dict['data']+thisMonth_volume_accumulate_dict['data']
                    
                    write_csv (stock_id,directory, filename, lastMonth_highLow_accumulate_dict,lastMonth_volume_accumulate_dict,IsFirSecDay)    # write files into CSV
                    time.sleep(1)  
                    
                #Jan 1 and Jan 2
                elif((today=='1' or today=='2') and str(thisMonth)=='1'):
                    
                    #get the stock data from last month
                    lastMonth_highLow_accumulate_dict,lastMonth_volume_accumulate_dict = get_webmsg(stock_id,int(thisYear)-1,12)           #put the data into smt 
                    
                    makedirs (stock_id)                  #create directory function
                    
                    time.sleep(1)
                    
                    
                    #get the stock data of this month      
                    thisMonth_highLow_accumulate_dict,thisMonth_volume_accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth)           #put the data into smt 
                    
                    #combine the stock data of this month and last month
                    lastMonth_highLow_accumulate_dict['data'] = lastMonth_highLow_accumulate_dict['data']+thisMonth_highLow_accumulate_dict['data']
                    lastMonth_volume_accumulate_dict['data'] = lastMonth_volume_accumulate_dict['data']+thisMonth_volume_accumulate_dict['data']
                            
                    write_csv (stock_id,directory, filename, lastMonth_highLow_accumulate_dict,lastMonth_volume_accumulate_dict,IsFirSecDay)    # write files into CSV
                    time.sleep(1) 
                else:    
                    #general date situation    
                    highLow_accumulate_dict,volume_accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth)           #put the data into smt 
                    #print(accumulate_dict)
                    makedirs (stock_id) 
                    write_csv (stock_id,directory, filename, highLow_accumulate_dict,volume_accumulate_dict)    # write files into CSV
                    time.sleep(1)    

                
            


            
            














def setFeatureData(stock_id,thisYear,thisMonth,today):
   
           
            '''
            juristicYear=str(int(thisYear)-1911)

            url= 'https://stock.wearn.com/netbuy.asp?Year='+juristicYear+'&month='+"{0:0=2d}".format(thisMonth)+'&kind='+str(stock_id)
            #print(url)
            dfs=pd.read_html(url)
            juristicPerson=dfs[0]

            juristicPerson=juristicPerson.iloc[:,1:]
            juristicPerson=juristicPerson.drop(juristicPerson.index[[0,1]])
            juristicPerson = juristicPerson.iloc[::-1]







           
            juristicPerson.columns=[u'投信',u'自營商',u'外資']
            
            #get the latest feature_days's juristic person data
            juristicPerson=juristicPerson.tail(feature_days)
            juristicPerson=juristicPerson.reset_index(drop=True)
            #print(juristicPerson)
            '''


            # read stock data of the current iterated company 
            stockDataFilePath='./ParsedStock'+'/ParsedTestingData_'+str(stock_id) +'/'+ str(thisMonth)+'_'+today+'.csv'   
            #while not os.path.exists(stockDataFilePath):
            #    time.sleep(1)

            if os.path.isfile(stockDataFilePath):
                # read stock data of the current iterated company 
                stockData = pd.read_csv(stockDataFilePath)
                '''
                #/#with 成交量
                #stockData=stockData.iloc[:,2:9]
                
                #/#without 成交量
                stockData=stockData.iloc[:,3:8]
                
                #get the latest feature_days's juristic person data
                stockData=stockData.tail(feature_days)
                stockData=stockData.reset_index(drop=True)
                #print(stockData)

                featureData = pd.concat([stockData,juristicPerson ], axis=1)
                
                #print(featureData)
                #send featureData back to main function
                return featureData  
                '''
                return stockData 
            
            else:
                raise ValueError("%s isn't a file!" % stockDataFilePath)
        
                       

       
    
#write pandas dataframe to csv file               
def writeTestingDataSet2csv(DataFrame,stock_id,testingDataFilename):
    
    testingDataDirectory='./ParsedStock/TestingDataSet/'+str(stock_id)+'_testingDataSet'
    if not os.path.exists(testingDataDirectory):
        os.makedirs(testingDataDirectory)
    #store training data set to csv
    DataFrame.to_csv(testingDataDirectory+'/'+testingDataFilename+'.csv', index=False)

    
    
def setupTestingDataSetFormat(testingData):
   
    
    
   
    #create empty pandas dataframe as a container for testing data set
    testingDataSet = pd.DataFrame()
  
    #declare an empty pandas container as container
    aRecordOfTrainingData=pd.DataFrame()
    
    dayCounter=feature_days
    numOfTestingDataRow=testingData.shape[0]
    print(numOfTestingDataRow)
    #setup features and label them with the data of the past feature_days days
    for row_index in range( numOfTestingDataRow-feature_days,numOfTestingDataRow):
        
        
        
        #get the stock data of the previous feature_days days and reset their index to merge them in the same row in later merge process.
        df_previousDay = testingData.iloc[[row_index]]
        df_previousDay=df_previousDay.reset_index(drop=True)
        
       
        daysBefore=str(dayCounter)
        dayCounter=dayCounter-1
        #/#with 成交量
        #df_previousDay.columns = [daysBefore+u'天前成交金額',daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前成交筆數',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']
        
         #/#without 成交量
        
        df_previousDay.columns = [daysBefore+u'天前開盤指數',daysBefore+u'天前最高指數',daysBefore+u'天前最低指數',daysBefore+u'天前收盤指數',daysBefore+u'天前成交股數',daysBefore+u'天前成交金額',daysBefore+u'天前成交筆數',daysBefore+u'天前漲跌點數']

        testingDataSet=pd.concat([testingDataSet,df_previousDay], axis=1)
   
        
        
        #add a record of feature and label to testingDataSet  
    #testingDataSet=pandas.concat([testingDataSet, aRecordOfTrainingData])
    
    
    return testingDataSet
def  rearrange2SVMFormat(testingDataSet):
        #get num of cols
        numOfCol=len(testingDataSet.columns)
        #rearrange to libSVM training data format
        for index, row in testingDataSet.iterrows():

            for colNo in range(0,numOfCol):
                testingDataSet.loc[index,list_colName[colNo]]=str(colNo+1)+':'+str( testingDataSet.loc[index,list_colName[colNo]])
        
        #insert the unknown RiseOrFall col to testing data set
        new_col = [0]  # can be a list, a Series, an array or a scalar   
        testingDataSet.insert(0, column='RiseOrFall', value=new_col)
        return testingDataSet
    
#write pandas dataframe to csv file               
def writeSVMFormat2Csv(DataFrame,stock_id,testingDataFilename):
    #store training data set to csv
   
    testingDataDirectory='./ParsedStock/TestingDataSet/LIBSVM'+str(stock_id)+'_testingDataSet'
    if not os.path.exists(testingDataDirectory):
        os.makedirs(testingDataDirectory)
    #store training data set to csv
    DataFrame.to_csv(testingDataDirectory+'/'+str(stock_id)+'_'+testingDataFilename+'.csv', index=False, sep=" ",header=False, encoding='utf-8')

def buildTestingDataSet():
        #update date time info every day
        now = datetime.datetime.now()
        
        thisYear=str(now.year)
        thisMonth=now.month
        today=str(now.day)
       
        #set the filename of tesing data
        tomorrowDate = now + datetime.timedelta(days=1)
       
        testingDataFilename=str(tomorrowDate.year)+'-'+str(tomorrowDate.strftime('%m'))+'-'+str(tomorrowDate.strftime('%d'))

        #get stock data and store it as csv 
        getStockData(thisYear,thisMonth,today)

        
        for year in year_list:
            
            #setup all the features
            featureData=setFeatureData(year,thisYear,thisMonth,today)


            #setup testing data set
            testingDataSet=setupTestingDataSetFormat(featureData)

            #write pandas dataframe to csv file for clf usage 
            writeTestingDataSet2csv(testingDataSet,year,testingDataFilename)
            
            
            
            #Generate SVM testing Data format
            #rearrange dataframe to libSVM testing data format
            testingDataSet=rearrange2SVMFormat(testingDataSet)
            
            #write to csv and replace comma with space
            writeSVMFormat2Csv(testingDataSet,year,testingDataFilename)
        
        
        
        #restart timer again to at 16:30 the next day 
        #/#
        '''
        everyDayExecuter = Timer(secs, buildTestingDataSet)
        everyDayExecuter.start()
        '''


def main():
    #/#manually execution
    buildTestingDataSet()
     
 
    
    
    #start the timer to run program at 16:30 every day,after it stops, restart it in the buildTestingDataSet function
    #/
    #everyDayExecuter = Timer(secs, buildTestingDataSet)#A threading.Timer executes a function once. 
    #everyDayExecuter.start()
     
    
if __name__ == "__main__":
    main()
