# coding: utf-8

# In[9]:

import requests
import json
import csv
import time, datetime,os,shutil
from bs4 import BeautifulSoup
import pandas
# In[10]:

dt = datetime.datetime.now()
dt.year
dt.month
thisYear=2017

# In[11]:

#id_list = ['2303','2330','1234','3006','2412'] #inout the stock IDs
id_list = ['2331','2330'
] #inout the stock IDs
now = datetime.datetime.now()
#year_list = range (2007,now.year+1) #since 2007 to this year
year_list = range (thisYear,now.year+1) #since 2007 to this year
#month_list = range(1,13)  # 12 months
month_list = range(1,4)  # 1-9 month
# In[12]:




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


# In[13]:

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


# In[14]:

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



# In[15]:
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
            


            
            












juristicYear_list = range ((thisYear-1911),(now.year+1)-1911) #since 2007 to this year

def main():
    
    #get stock data and store it as csv 
    getStockData()
    
    #setup training data 
    for stock_id in id_list:
        
       
        
        #set up empty pandas dataframe as container
        accumulateJuristic = pandas.DataFrame()
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


            # read stock data of the current iterated company 
            stockDataFilePath='./ParsedStock/'+str(stock_id)+'/'+ADYear+'StockData/'+ADYear+'.csv'
            #while not os.path.exists(stockDataFilePath):
            #    time.sleep(1)

            if os.path.isfile(stockDataFilePath):
                # read stock data of the current iterated company 
                stockData = pandas.read_csv(stockDataFilePath)

                stockData=stockData.iloc[:,3:8]

                trainingData = pandas.concat([stockData,accumulateJuristic ], axis=1)
                #store to training data csv

                #without column name
                #trainingData.to_csv('bin/ParsedStock/'+str(stock_id)+'_trainingData.csv', index=False,header=False)
                trainingData.to_csv('./ParsedStock/'+str(stock_id)+'_trainingData.csv', index=False)

            else:
                raise ValueError("%s isn't a file!" % './ParsedStock/'+str(stock_id)+'/'+ADYear+'StockData/'+ADYear+'.csv')

if __name__ == "__main__":
    main()