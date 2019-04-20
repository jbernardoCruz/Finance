# Plot Libs
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_finance import candlestick_ohlc
from uAI_typedef import*

plt.style.use('ggplot')

def plot_scatter3D(data, y):
    fig = plt.figure()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    '''
    ax.scatter(data[:, 0], data[:, 1], data[:, 2],
        c=y, edgecolor='k')
    '''
    ax.scatter(data[:, 0], data[:, 1], data[:, 2],
                c=y, edgecolor='k')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    #ax.dist = 12
    plt.show()

def plot_candleStick(ax, data, vol):
    ''' 
    - Plot Candlestick and Volume \n
    Parameters:
    ----------
    [in] data = ['time', 'open', 'high', 'low', 'close'] \n
    [in] vol = ['vol']
    '''
    ax.xaxis_date()
    candlestick_ohlc(ax, data.values, width=0.02, colorup='g', colordown='#e60000')

    '''
    ax2 = plt.subplot2grid((9,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax2.fill_between(data[TIME].values , vol, 0, color='b')
    '''
def plot_bollingerBands(ax, time, bb):
    '''
    - Plot Bollinger Bands \n
    Parameters:
    ----------
    [in] ax = axis \n
    [in] time = time \n
    [in] bb = df'[BB_UP', 'BB_MED', 'BB_LOW'] 
    '''
    ax.plot(time, bb[BB_UP].values, color=CYAN, linewidth=1 , linestyle='--')
    ax.plot(time, bb[BB_MED].values, color=CYAN, linewidth=1 , linestyle='--')
    ax.plot(time, bb[BB_LOW].values, color=CYAN, linewidth=1 , linestyle='--')

def plot_rsi(ax, time, *rsi):
    '''
    - Plot RSI (Relative Strength Index) \n
    Parameters:
    ----------
    [in] ax = axis \n
    [in] time = time \n
    [in] *rsi = df['RSI']
    '''
    for i,rsi_aux in enumerate(rsi):
        if i==0: color=BLACK; linewidth=1.5
        elif i==1: color=CYAN; linewidth=1
        elif i==2: color=RED; linewidth=1
        ax.plot(time, rsi_aux, color=color, linewidth=linewidth)
        ax.xaxis_date()
        ax.axhline(RSI_OVERBOUGHT, color=WHITE, linestyle='--')
        ax.axhline(RSI_OVERSOLD, color=WHITE, linestyle='--')
        #ax.fill_between(time, rsi, 70, where=(rsi <= 70), facecolor=WHITE, edgecolor=WHITE)
        #ax.fill_between(time, rsi, 30, where=(rsi >= 30), facecolor=WHITE, edgecolor=WHITE)
        textsize = 9
        ax.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax.transAxes, fontsize=textsize)
        ax.text(0.6, 0.1, '<30 = oversold', transform=ax.transAxes, fontsize=textsize)
        ax.set_ylim(0, 100)
        ax.set_yticks([RSI_OVERSOLD, RSI_OVERBOUGHT])

def plot_SRSI(ax, time, s_rsi):
    '''
    - Plot S_RSI (Stochastic RSI) \n
    Parameters:
    ----------
    [in] ax = axis \n
    [in] time = time \n
    [in] s_rsi = df['S_RSI_K', 'S_RSI_D']
    '''
    ax.plot(time, s_rsi[S_RSI_K].values, color=CYAN, linewidth=1)
    ax.plot(time, s_rsi[S_RSI_D].values, color=ORANGE, linewidth=1)
    ax.xaxis_date()
    ax.axhline(S_RSI_OVERBOUGHT, color=WHITE, linestyle='--')
    ax.axhline(S_RSI_OVERSOLD, color=WHITE, linestyle='--')
    ax.set_ylim(-10, 110)
    ax.set_yticks([S_RSI_OVERSOLD, S_RSI_OVERBOUGHT])

#ax1.annotate('{},{}'.format(x,y), xy=(x, y))