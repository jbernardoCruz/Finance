from uAI_lib import getData, loadDataFromCSV, timeStampToDate, saveCSV
from uAI_plot import plot_candleStick
from uAI_Finance import Finance
from uAI_typedef import *

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='jbernardoCruz', api_key='wLC85rHSk0rclw6QbkAn')

'''LOAD DATA'''
timeFrame = 15
coin = 'ETHUSD'
fileName = 'data_test.csv'
csvData = loadDataFromCSV(fileName, [TIME, OPEN, HIGH, LOW, CLOSE, VOL])
finance = Finance(csvData)
data = finance.data


#Price
price_graph = go.Candlestick(x=data[TIME], open=data[OPEN], high=data[HIGH], low=data[LOW],close=data[CLOSE], name=str(coin))

rsiUp = []
rsiLow = []
for i in range(len(finance.rsi)):
    rsiUp.append(70)
    rsiLow.append(30)

    
colors = ['rgb(67,67,67)', 'rgb(49,130,189)']
#RSI
rsi_graph = go.Scatter(x = data[TIME], y = finance.RSI(),  name='RSI',  mode='lines', line=dict(color=colors[0]))
rsiUp_graph = go.Scatter(x = data[TIME], y = rsiUp, name='', mode='lines', line=dict(color=colors[1]))
rsiLow_graph = go.Scatter(x = data[TIME], y = rsiLow, name='', mode='lines', line=dict(color=colors[1]))

y = finance.S_RSI()


teste = y[S_RSI_K]


print("Teste")