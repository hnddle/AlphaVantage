import pandas

from alpha_vantage.timeseries import TimeSeries  # Stock Time Series
from alpha_vantage.foreignexchange import ForeignExchange  # Forex (FX)
from alpha_vantage.cryptocurrencies import CryptoCurrencies  # Cryptocurrencies
from alpha_vantage.techindicators import TechIndicators  # TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances  # Sector Performances

import os
import io
import requests
import re
import sys
import time
from functools import wraps
import inspect
import matplotlib.pyplot as plt
from datetime import date, timedelta
import pandas as pd
import threading

watchList = pd.read_csv('E:/Investing/watchList.csv', index_col=0)

for i in range(len(watchList['Code'])):
    data = pd.read_csv('E:/Investing/Data/{0}.csv'.format(watchList['Code'][i]))

    data['4. close'].plot()
    plt.title('Daily Adjusted Times Series for the {0} stock (1 min)'.format(watchList['Code'][i]))
    plt.show()

