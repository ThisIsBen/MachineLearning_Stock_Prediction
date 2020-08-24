# coding: utf-8

import requests
import json
import csv
import time,datetime,os,shutil
from bs4 import BeautifulSoup
import pandas
import sys
from threading import Timer


######parameter area
#id_list = ['2303','2330','1234','3006','2412'] #inout the stock IDs
id_list = ['2317','2330','2885'] 



#use the past 3 days' data to predict next day's stock
feature_days=3
    
#without 'RiseOrFall'

#/#with 成交量
#list_colName=[u'3天前成交金額',u'3天前開盤價',u'3天前最高價',u'3天前最低價',u'3天前收盤價',u'3天前漲跌價差',u'3天前成交筆數',u'3天前投信',u'3天前自營商',u'3天前外資',u'2天前成交金額',u'2天前開盤價',u'2天前最高價',u'2天前最低價',u'2天前收盤價',u'2天前漲跌價差',u'2天前成交筆數',u'2天前投信',u'2天前自營商',u'2天前外資',u'1天前成交金額',u'1天前開盤價',u'1天前最高價',u'1天前最低價',u'1天前收盤價',u'1天前漲跌價差',u'1天前成交筆數',u'1天前投信',u'1天前自營商',u'1天前外資']




#/#without 成交量
list_colName=[u'3天前開盤價',u'3天前最高價',u'3天前最低價',u'3天前收盤價',u'3天前漲跌價差',u'3天前投信',u'3天前自營商',u'3天前外資',u'2天前開盤價',u'2天前最高價',u'2天前最低價',u'2天前收盤價',u'2天前漲跌價差',u'2天前投信',u'2天前自營商',u'2天前外資',u'1天前開盤價',u'1天前最高價',u'1天前最低價',u'1天前收盤價',u'1天前漲跌價差',u'1天前投信',u'1天前自營商',u'1天前外資']
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
        firstMonth=True
        accumulate_dict = {}
   
        date = thisYear + "{0:0=2d}".format(thisMonth) +'01' ## format is yyyymmdd
        sid = str(stock_id)
        url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+sid
        #print(url_twse)
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




def write_csv(stock_id,directory,filename,smt,IsFirSecDay=False) :
    writefile = directory + filename               #set output file name
    #outputFile = open(writefile,'w',newline='')
    outputFile = open(writefile,'a',newline='')#append to the file
    outputWriter = csv.writer(outputFile)
    '''
    head = ''.join(smt['title'].split())
    a = [head,""]
    outputWriter.writerow(a)
    '''
    #print(smt)
    #if today is the first or the second day on a month
    if(IsFirSecDay==False):
        outputWriter.writerow(smt['fields']) #write header 
        
    
    for data in (smt['data']):
        outputWriter.writerow(data)

    outputFile.close()




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

    for stock_id in id_list:
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
                    accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth-1)           #put the data into smt 
                    #print(accumulate_dict)
                    makedirs (stock_id)                  #create directory function
                    write_csv (stock_id,directory, filename, accumulate_dict)    # write files into CSV
                    time.sleep(1)
                    
                    
                    #general date situation    
                    accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth)           #put the data into smt 
                    #print(accumulate_dict)         
                    write_csv (stock_id,directory, filename, accumulate_dict,IsFirSecDay)    # write files into CSV
                    time.sleep(1)  
                    
                #Jan 1 and Jan 2
                elif((today=='1' or today=='2') and str(thisMonth)=='1'):
                    accumulate_dict = get_webmsg(stock_id,int(thisYear)-1,12)           #put the data into smt 
                    #print(accumulate_dict)
                    makedirs (stock_id)                  #create directory function
                    write_csv (stock_id,directory, filename, accumulate_dict)    # write files into CSV
                    time.sleep(1)
                    
                    
                    #general date situation    
                    accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth)           #put the data into smt 
                    #print(accumulate_dict)         
                    write_csv (stock_id,directory, filename, accumulate_dict,IsFirSecDay)    # write files into CSV
                    time.sleep(1) 
                else:    
                    #general date situation    
                    accumulate_dict = get_webmsg(stock_id,thisYear,thisMonth)           #put the data into smt 
                    #print(accumulate_dict)
                    makedirs (stock_id) 
                    write_csv (stock_id,directory, filename, accumulate_dict)    # write files into CSV
                    time.sleep(1)    

                
            


            
            














def setFeatureData(stock_id,thisYear,thisMonth,today):
   
           
            
            juristicYear=str(int(thisYear)-1911)

            url= 'https://stock.wearn.com/netbuy.asp?Year='+juristicYear+'&month='+"{0:0=2d}".format(thisMonth)+'&kind='+str(stock_id)
            #print(url)
            dfs=pandas.read_html(url)
            juristicPerson=dfs[0]

            juristicPerson=juristicPerson.iloc[:,1:]
            juristicPerson=juristicPerson.drop(juristicPerson.index[[0,1]])
            juristicPerson = juristicPerson.iloc[::-1]







           
            juristicPerson.columns=[u'投信',u'自營商',u'外資']
            
            #get the latest feature_days's juristic person data
            juristicPerson=juristicPerson.tail(feature_days)
            juristicPerson=juristicPerson.reset_index(drop=True)
            #print(juristicPerson)
            


            # read stock data of the current iterated company 
            stockDataFilePath='./ParsedStock'+'/ParsedTestingData_'+str(stock_id) +'/'+ str(thisMonth)+'_'+today+'.csv'   
            #while not os.path.exists(stockDataFilePath):
            #    time.sleep(1)

            if os.path.isfile(stockDataFilePath):
                # read stock data of the current iterated company 
                stockData = pandas.read_csv(stockDataFilePath)

                #/#with 成交量
                #stockData=stockData.iloc[:,2:9]
                
                #/#without 成交量
                stockData=stockData.iloc[:,3:8]
                
                #get the latest feature_days's juristic person data
                stockData=stockData.tail(feature_days)
                stockData=stockData.reset_index(drop=True)
                #print(stockData)

                featureData = pandas.concat([stockData,juristicPerson ], axis=1)
                
                #print(featureData)
                #send featureData back to main function
                return featureData     
            
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
    testingDataSet = pandas.DataFrame()
  
    #declare an empty pandas container as container
    aRecordOfTrainingData=pandas.DataFrame()

    
    dayCounter=feature_days
    numOfTestingDataRow=testingData.shape[0]
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
        df_previousDay.columns = [daysBefore+u'天前開盤價',daysBefore+u'天前最高價',daysBefore+u'天前最低價',daysBefore+u'天前收盤價',daysBefore+u'天前漲跌價差',daysBefore+u'天前投信',daysBefore+u'天前自營商',daysBefore+u'天前外資']

        testingDataSet=pandas.concat([testingDataSet,df_previousDay], axis=1)
   
        
        
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
    DataFrame.to_csv(testingDataDirectory+'/'+str(stock_id)+'_'+testingDataFilename+'.csv', index=False, sep=" ",header=False)

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


        for stock_id in id_list:
            #setup all the features
            featureData=setFeatureData(stock_id,thisYear,thisMonth,today)


            #setup testing data set
            testingDataSet=setupTestingDataSetFormat(featureData)

            #write pandas dataframe to csv file for clf usage 
            writeTestingDataSet2csv(testingDataSet,stock_id,testingDataFilename)
            
            
            
            #Generate SVM testing Data format
            #rearrange dataframe to libSVM testing data format
            testingDataSet=rearrange2SVMFormat(testingDataSet)
            
            #write to csv and replace comma with space
            writeSVMFormat2Csv(testingDataSet,stock_id,testingDataFilename)
          
        #restart timer again to at 16:30 the next day 
        #/#
        '''
        everyDayExecuter = Timer(secs, buildTestingDataSet)
        everyDayExecuter.start()
        '''
    


def main():
    #/#manually execution
    #buildTestingDataSet()
     
 
    
    
    #start the timer to run program at 16:30 every day,after it stops, restart it in the buildTestingDataSet function
    #/#
    everyDayExecuter = Timer(secs, buildTestingDataSet)#A threading.Timer executes a function once. 
    everyDayExecuter.start()
     
    
if __name__ == "__main__":
    main()
