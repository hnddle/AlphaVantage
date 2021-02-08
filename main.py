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

# API Key, TimeSeries 생성
keyFile = open('E:/Investing/Settings/apiKey.txt', 'r')
api_key = keyFile.read()
app = TimeSeries(key=api_key, output_format='pandas')
update = False

# holdings_df.to_csv('E:/Data/holdings.csv')
# watchList_df.to_csv('E:/Data/watchList.csv')
holdings = pd.read_csv('E:/Investing/holdings.csv', index_col=0)
watchList = pd.read_csv('E:/Investing/watchList.csv', index_col=0)

# 마지막 업데이트 일자 확인
updated = open('E:/Investing/Settings/updatedDate.txt', 'r')
lastDate = updated.read()
if lastDate == str(date.today()) or update == False:
    renew = False
else:
    renew = True
updated.close()

# 업데이트 수행
if renew:
    for i in range(len(watchList['Code'])):
        data, meta_data = app.get_daily_adjusted(watchList['Code'][i], outputsize='full')
        data.to_csv('E:/Investing/Data/{0}.csv'.format(watchList['Code'][i]))
        # 1분 5건, 1일 500건 제한이기 때문
        time.sleep(15)
    updated = open('E:/Investing/Data/updatedDate.txt', 'w')
    updated.write(str(date.today()))
    updated.close()

df_ls = []

sumTotalPrice = 0

for i in range(len(watchList['Code'])):
    ls = []
    Code = watchList['Code'][i]
    Name = watchList['Name'][i]
    TargetRate = watchList['TargetRate'][i]
    quantity = 0
    buyPrice = 0.0
    totalBuyPrice = 0.0
    totalPrice = 0.0

    if watchList['Code'][i] in holdings['Code'].values:
        for j in range(len(holdings['Code'])):
            if watchList['Code'][i] == holdings['Code'][j]:
                quantity = holdings['Quantity'][j]
                buyPrice = holdings['BuyPrice'][j]
                totalBuyPrice = quantity * buyPrice

    data = pd.read_csv('E:/Investing/Data/{0}.csv'.format(watchList['Code'][i]))
    currentPrice = data['4. close'][0]
    totalPrice = currentPrice * quantity
    sumTotalPrice += totalPrice
    sumTotalPrice = 142857

    ls.append(Code)
    ls.append(Name)
    ls.append(quantity)  # 보유량
    ls.append(buyPrice)  # 매수가
    ls.append(currentPrice)  # 현재가
    ls.append(round(totalBuyPrice, 2))  # 매수총액
    ls.append(round(totalPrice, 2))  # 현재총액
    ls.append(TargetRate)  # 목표비율
    ls.append(0.0)  # 현재비율
    ls.append(0.0)  # 필요량
    ls.append(False)  # 조정대상
    df_ls.append(ls)

result_df = pd.DataFrame(df_ls,
                         columns=['Code', 'Name', 'Quantity', 'BuyPrice', 'CurrentPrice', 'TotalBuyPrice',
                                  'TotalPrice', 'TargetRate', 'CurrentRate', 'AdjustCount', 'AdjustTarget'])
count = 0
for index, row in result_df.iterrows():
    totalDiff = ((row['TargetRate'] * sumTotalPrice) - row['TotalPrice'])
    if row['TotalPrice'] == 0:
        rateDiff = 0
    else:
        rateDiff = (row['TargetRate'] * sumTotalPrice) / row['TotalPrice']
    result_df['CurrentRate'][count] = round(row['TotalPrice'] / sumTotalPrice, 2)
    result_df['AdjustCount'][count] = round(totalDiff / row['CurrentPrice'], 2)

    if rateDiff > 1.2 or rateDiff < 0.8:
        result_df['AdjustTarget'][count] = True
    else:
        result_df['AdjustTarget'][count] = False

    count = count + 1

result_df.to_csv('E:/Investing/result.csv')


