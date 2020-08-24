# coding: utf-8

# In[9]:

import requests
import json
import csv
import time, datetime,os
from bs4 import BeautifulSoup
import pandas

# In[10]:

#########parameter area
#id_list = ['2303','2330','1234','3006','2412'] #inout the stock IDs
#id_list = ['2317','2330'] #inout the stock IDs
id_list = ['2317','2330','2885']
#use the past 3 days' data to predict next day's stock
feature_days=3

#/#with 成交量
#list_colName=[u'3天前成交金額',u'3天前開盤價',u'3天前最高價',u'3天前最低價',u'3天前收盤價',u'3天前漲跌價差',u'3天前成交筆數',u'3天前投信',u'3天前自營商',u'3天前外資',u'2天前成交金額',u'2天前開盤價',u'2天前最高價',u'2天前最低價',u'2天前收盤價',u'2天前漲跌價差',u'2天前成交筆數',u'2天前投信',u'2天前自營商',u'2天前外資',u'1天前成交金額',u'1天前開盤價',u'1天前最高價',u'1天前最低價',u'1天前收盤價',u'1天前漲跌價差',u'1天前成交筆數',u'1天前投信',u'1天前自營商',u'1天前外資','RiseOrFall']


#/#without 成交量

list_colName=[]
for daysBefore in range (feature_days,0,-1):
    daysBefore=str(daysBefore)
    list_colName.append(daysBefore+u'天前開盤價')
    list_colName.append(daysBefore+u'天前最高價')
    list_colName.append(daysBefore+u'天前最低價')
    list_colName.append(daysBefore+u'天前收盤價')
    list_colName.append(daysBefore+u'天前漲跌價差')
    list_colName.append(daysBefore+u'天前投信')
    list_colName.append(daysBefore+u'天前自營商')
    list_colName.append(daysBefore+u'天前外資')
list_colName.append('RiseOrFall')

list_trainingSetType=['classifier','riseRegressor','fallRegressor']

list_ClfOrRg=['CLF','RiseRg','FallRg']
#########parameter area

#write pandas dataframe to csv file               
def writeTrainingDataSet2Csv(DataFrame,stock_id,ClfOrRg):
    #store training data set to csv
    DataFrame.to_csv('./ParsedStock/TrainingDataSet/LIBSVM'+str(stock_id)+ClfOrRg+'_trainingDataSet.csv', index=False,sep=" ",header =False)

def moveACol2Front(DataFrame):
    cols = list(DataFrame)
    # move the column to head of list using index, pop and insert
    cols.insert(0, cols.pop(cols.index('RiseOrFall')))
    DataFrame = DataFrame.ix[:, cols]
    return DataFrame

def rearrange2LIBSVMFormat(stock_id,trainingSetType,ClfOrRg):
        TrainingData=pandas.read_csv('./ParsedStock/TrainingDataSet/'+str(stock_id)+'_'+trainingSetType+'_trainingDataSet.csv')
        #get num of cols
        numOfCol=len(TrainingData.columns)-1

        #rearrange to libSVM training data format
        for index, row in TrainingData.iterrows():

            for colNo in range(0,numOfCol):
                TrainingData.loc[index,list_colName[colNo]]=str(colNo+1)+':'+str( TrainingData.loc[index,list_colName[colNo]])
                
        
        
        
        #Move RiseORFall to the front
        TrainingData=moveACol2Front(TrainingData)
        
        #write to csv and replace comma with space
        writeTrainingDataSet2Csv(TrainingData,stock_id,ClfOrRg)
        

def main():
    
    numOfModel=len(list_trainingSetType)
    for stock_id in id_list:
        for i in range (0,numOfModel):
            rearrange2LIBSVMFormat(stock_id,list_trainingSetType[i],list_ClfOrRg[i])
        
        

if __name__ == "__main__":
    main()
