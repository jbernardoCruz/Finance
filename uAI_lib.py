import requests
import pandas as pd
from uAI_typedef import *
from datetime import datetime
from matplotlib.dates import date2num

REQUEST_SUCCES = 200

# Get Data from BITFINEX 
def getData(interval, cryptoCoin, days):
  ''' Get Data from BITFINEX '''  
  data = []
  days = str(days)
  address = str('https://api.bitfinex.com/v2/candles/trade:'+ interval + ':t'+ cryptoCoin +'/hist?&limit='+ days)
  print("Requesting Data: " + address)
  r = requests.get(address)
  if (r.status_code == REQUEST_SUCCES): 
      print("\nData successfully acquired")
      result = r.json()
      data = result             
  return data

# Save data into a CSV file
def saveCSV(data, fileName):
  ''' Save data into a CSV file ''' 
  print("\nSaving .csv file...")
  fileName = str(fileName)
  with open(fileName, 'w') as file:
      file.write("TIME,OPEN,HIGH,LOW,CLOSE,VOL\n")
      for i in data:
        file.write(str(i[0]) + ',' +
                    str(i[1]) + ',' +
                    str(i[3]) + ',' +
                    str(i[4]) + ',' +
                    str(i[2]) + ',' +
                    str(int(i[5])) + '\n')
  print("\nFile saved: "+ fileName+ "\n")

def reverseDataFrame(dataFrame):  
  dataFrame.iloc[:] = dataFrame.iloc[::-1].values 
  return  dataFrame

def timeStampToDate(dataFrame):  
  ''' Get data given a Timestamp '''
  dates = []
  timeStamp_list = dataFrame.tolist()
  for timeStamp in timeStamp_list:
      timeStamp = int(timeStamp/1000)
      dtime = datetime.utcfromtimestamp(timeStamp)
      dates.append(dtime.strftime('%Y-%m-%d %H:%M:%S'))
  dates_out = pd.DataFrame(dates, columns=['Date'])
  dates_out.loc[:, 'Date'] = pd.to_datetime(dates_out['Date'], format='%Y-%m-%d %H:%M:%S') 
  return dates_out

# Load data (Dataframe) from a CSV file	
def loadDataFromCSV(csvFile, colName):
  ''' Load data (Dataframe) from a CSV file '''
  dataFrame = pd.read_csv(csvFile)
  dataFrame.columns = colName
  dataFrame['TIME'] = dataFrame['TIME'].astype('int64')   
  data = reverseDataFrame(dataFrame)
  data[TIME] = date2num(timeStampToDate(data[TIME]))

  return  data