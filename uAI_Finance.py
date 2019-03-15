''' Module that provided Finance Indicators '''
import pandas as pd
import numpy as np
from sklearn import cluster
from uAI_typedef import *

# FINANCE CLASS
class Finance():

  ''' FINANCE CLASS '''

  def __init__(self, data):
    self.data = data
    self.set_RSI()
    self.set_BollingerBands()
    self.set_BBP()
    self.set_S_RSI()
    
    print ("\nFinance data set.")

  # Calculate EMA
  def EMA(self, days, type='df'):
    ''' 
    - Calculates EMA (Exponential Moving Average)\n
    Parameters:
    ----------
    [in] days = interval \n
    [in] type = 'df' (default) or 'mat' \n
    [out] df['EMA']
    '''
    data = self.data[CLOSE]
    ema = pd.DataFrame()
    ema[EMA] = data.ewm(span=days, adjust=False).mean() 
    return self.returnValue(ema, type)

  # Set EMA  
  def set_EMA(self, days):    
    ''' 
    - Set EMA (Exponential Moving Average) \n
    Parameters:
    ----------
    [in] days = interval 
    '''
    ema = pd.DataFrame(columns=[EMA+str(days)])
    ema = self.EMA(days)
    self.data.join(ema)

  # Calculate SMA 
  def SMA(self, days, type='df'):
    ''' 
    - Calculates SMA (Simple Moving Average) \n  
    Parameters:
    ---------- 
    [in] days = interval \n
    [in] type = 'df' (default) or 'mat' \n
    [out] df['SMA']   
    '''
    data = self.data[CLOSE]
    sma = pd.DataFrame()
    sma[SMA] = data.rolling(days).mean()
    return self.returnValue(sma, type)

  # Set SMA  
  def set_SMA(self, days):
    ''' 
    - Set SMA (Simple Moving Average) \n
    Parameters:
    ----------
    [in] days = interval
    '''
    sma = pd.DataFrame(columns=[SMA+str(days)])
    sma = self.SMA(days)
    self.data.join(sma)

  # Calculate MACD EMA
  def MACD_EMA(self, macd):
    ''' 
    - Calculates MACD EMA 
    '''
    ema = macd.ewm(span=9, adjust=False).mean()
    return ema

 # Calculate MACD 
  def MACD(self, type='df'):
    ''' 
    - Calculates MACD \n
    Parameters:
    ----------
    [in] type = 'df' (default) or 'mat'  \n
    [out] df['MACD', 'SIGNAL', 'HIST']  \n
    '''
    macd = self.EMA(12) - self.EMA(26)
    signal = self.MACD_EMA(macd)
    macd_hist = macd.as_matrix() - signal.as_matrix()
    
    macd_out = pd.DataFrame(columns = [MACD, MACD_S, MACD_H])
    macd_out[MACD] = macd
    macd_out[MACD_S] = signal
    macd_out[MACD_H] = macd_hist
    return self.returnValue(macd_out, type)

  # Set MACD 
  def set_MACD(self):
    ''' 
    - Set MACD 
    '''
    self.macd = self.MACD()

  # Calculate RSI 
  def RSI(self, period=14, type='df'):  
    ''' 
    - Calculates RSI (Relative Strenght Index)\n
    Parameters:
    ----------
    [in] type = 'df' (default) or 'mat' \n
    [out] df['RSI'] 
    '''
    data = self.data
    UpI = [0]  
    DoI = [0]  
    for i in range ((data[CLOSE].size)-1):
        change = data.get_value(i+1, CLOSE) - data.get_value(i, CLOSE)  
        if change >=0: UpD = change
        else: UpD = 0.0
        UpI.append(UpD)  
        if change < 0 : DoD = change*(-1)  
        else: DoD = 0.0  
        DoI.append(DoD)  

    UpI = pd.DataFrame(UpI)  
    DoI = pd.DataFrame(DoI)  
    alpha = 1/period
    avgGain = UpI.ewm(alpha=alpha, adjust=False).mean()
    avgLoss = DoI.ewm(alpha=alpha, adjust=False).mean()
    rs = avgGain / avgLoss

    rsi = np.array(100 - (100 / (1 + rs)))
    rsi_out = pd.DataFrame(rsi[:,0], columns=[RSI])

    return self.returnValue(rsi_out, type)

  # Set RSI 
  def set_RSI(self, period=14):  
    ''' 
    - Set RSI (Relative Strenght Index)
    '''
    self.rsi = self.RSI()

  # Calculate BB (Bollinger Bands)
  def BollingerBands(self, period=20, type='df'):
    ''' 
    - Calculates BB (Bollinger Bands) \n
    Parameters:
    ----------
    [in] type = 'df' (default) or 'mat' \n
    [out] df['BB_UP', 'BB_MED', 'BB_LOW']
    '''
    data = self.data[CLOSE]
    sma = data.rolling(window=period, min_periods=period - 1).mean()
    std = data.rolling(window=period, min_periods=period - 1).std()
    upper = (sma + (std * 2)).to_frame(BB_UP)
    lower = (sma - (std * 2)).to_frame(BB_LOW)
    medium = sma.to_frame(BB_MED)
    bb = pd.concat([lower, medium, upper], axis=1)
    return self.returnValue(bb, type)

  # Set BB (Bollinger Bands)
  def set_BollingerBands(self):
    '''
    - Set BB (Bollinger Bands) 
    '''
    self.bb = self.BollingerBands()

  def BBP(self, type='df'):
    '''
    - Calculate Bollinger Band %
    '''
    bbp = pd.DataFrame()

    bb = self.bb
    bbp['BBP'] = ((self.data[CLOSE] - bb[BB_LOW]) / (bb[BB_UP] - bb[BB_LOW]))
    return self.returnValue(bbp, type)

  def set_BBP(self):
    self.bbp = self.BBP()
    
  # Calculate Stochastic RSI (STOCH RSI)
  def S_RSI(self, period=14, type='df'):
    ''' 
    - Calculates Stochastic RSI (STOCH RSI) \n
    Parameters:
    ----------
    [in] type = 'df' (default) or 'mat'  \n
    [out] df['S_RSI_K', 'S_RSI_D']
    '''
    rsi = self.RSI()  
    rsi_aux = pd.DataFrame(rsi)
    high = rsi_aux.rolling(window=period).max()
    low = rsi_aux.rolling(window=period).min()

    stochRSI = pd.DataFrame()
    stochRSI[S_RSI_K] = ((rsi_aux - low) / (high - low))*100
    stochRSI[S_RSI_K] = stochRSI.rolling(window=3).mean()
    stochRSI[S_RSI_D] = stochRSI[S_RSI_K].rolling(window=3).mean()
    stochRSI = stochRSI.replace(np.NaN, 0)
    
    return self.returnValue(stochRSI, type)

  # Set Stochastic RSI (STOCH RSI)
  def set_S_RSI(self):
    '''
    - Set S_RSI (Stochastic RSI)
    '''
    self.s_rsi = self.S_RSI()
    pass

  def returnValue(self, value, type='df'):
    if type=='df': return value
    elif type=='mat':
      value = value.as_matrix()
      shape = value.shape
      if shape[1] == 1: return value[:,-1]
      else: return value

   # Calculate k-Means for a given number of Clusters
  def KMeans(self, n_clusters, data):
    ''' 
    - Calculates k-Means for a given number of Clusters 
    '''
    k_means = cluster.KMeans(n_clusters=n_clusters, random_state=0).fit(data)
    return k_means

  def saveData(self):
    ''' Save data into a CSV file ''' 
    print("\nSaving .csv file...")
    fileName = str('Finance.csv')
    with open(fileName, 'w') as file:
        file.write("INDEX,TIME,OPEN,HIGH,LOW,CLOSE,VOL,RSI,BBP\n")

        rsi = pd.DataFrame(self.rsi).fillna(0).as_matrix()
        bbp = pd.DataFrame(self.bbp).fillna(0).as_matrix()

        for i,data in self.data.iterrows():     
          file.write(str(i) + ',' +
                      str(data[TIME])+ ',' +
                      str(data[OPEN]) + ',' +
                      str(data[HIGH]) + ',' +
                      str(data[LOW]) + ',' +
                      str(data[CLOSE]) + ',' +
                      str(data[VOL]) + ',' +
                      str(rsi[i,0]) + ',' +
                      str(bbp[i,0]) + '\n')

    print("\nFile saved: "+ fileName+ "\n")
