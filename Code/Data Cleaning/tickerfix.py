'''
MSiA 400: Greenwich Project

This code was developed to clean the ticker data 
'''

import pandas as pd

#Load set of unique tickers from original data
uticks = pd.read_csv("uniqueTicks.csv")

#Fix issues that were found, such as stray numbers and forward slashes
uticks['fixticker'] = uticks['ticker']
uticks['fixticker'] = uticks['fixticker'].str.replace('\d+','')
uticks['fixticker'] = uticks['fixticker'].str.replace('\\','')


uticks = uticks[['fixticker']]
#drop empty tickers
uticks.drop(uticks[uticks['fixticker']==''].index, inplace = True) 

#Export valid and clean tickers
uticks.to_csv('prettyTicks2.csv',index=False)


