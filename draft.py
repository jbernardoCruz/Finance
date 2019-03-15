from uAI_lib import getData, loadDataFromCSV, timeStampToDate, saveCSV
from uAI_plot import plot_candleStick
from uAI_Finance import Finance
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DayLocator, DateFormatter
from uAI_plot import *
from uAI_typedef import *

'''
data = getData('1D', 'BTCUSD', 52)
saveCSV(data, '1d')
data = getData('1h', 'BTCUSD', 208)
saveCSV(data, '1h')
data = getData('15m', 'BTCUSD', 5000)
saveCSV(data, '15m')
'''

'''DATA'''
csvData = loadDataFromCSV('bitfinex15m.csv', [TIME, OPEN, HIGH, LOW, CLOSE, VOL])
data = Finance(csvData)

rsiOut = []
rsiOut.append(0)


for value in data.rsi['RSI']:  

    if value <= 30: rsiOut.append(1)
    elif (value > 30) and (value < 70): rsiOut.append(0)    
    elif value >= 70: rsiOut.append(-1)

bbpOutAux = []
for value in data.bbp['BBP']:
    if value <= 0: bbpOutAux.append(1)
    elif (value > 0) and (value < 1): bbpOutAux.append(0)    
    elif value >= 1: bbpOutAux.append(-1)

bbpOut = []
for i in range(18): bbpOut.append(-2)
bbpOut = bbpOut + bbpOutAux

output = []
index = []
for i,value in enumerate(rsiOut):

    if bbpOut[i] == 1 and rsiOut[i] != 1: output.append(0)
    elif bbpOut[i] == 1 and rsiOut[i] == 1: output.append(1)
    elif bbpOut[i] == -1 and rsiOut[i] != -1: output.append(0)
    elif bbpOut[i] == -1 and rsiOut[i] == -1: output.append(-1)

    else: output.append(0)
    
    index.append(i+1)


'''Plot'''
'''
plt.style.use('ggplot')

ax1 = plt.subplot2grid((13,1), (0,0), rowspan=7, colspan=1)
ax2 = plt.subplot2grid((13,1), (7,0), rowspan=3, colspan=1, sharex=ax1)
ax3 = plt.subplot2grid((13,1), (10,0), rowspan=3, colspan=1, sharex=ax1)
#ax4 = plt.subplot2grid((10,1), (21,0), rowspan=5, colspan=1, sharex=ax1)

plot_candleStick(ax1, data.data, data.data[VOL])
ax2.plot(data.data['TIME'], output, color=BLACK, linewidth=1.5)
ax3.plot(data.data['TIME'], data.rsi, color=BLUE, linewidth=1.5)

#ax3.plot(data.data[TIME], index, color=BLACK, linewidth=1.5)
#plot_rsi(ax3, data.data[TIME], data.rsi)
plt.show()
'''

data.saveData()




