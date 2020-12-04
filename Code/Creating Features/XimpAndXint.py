'''
MSiA 400: Greenwich Project

This code was developed to create the weight_Intern and weight_Important features.

'''

#!/usr/bin/env python
# coding: utf-8

import pandas as pd

#Initialize data files
titles = pd.read_csv("titles.csv")
tags = pd.read_csv("tags.csv")
timelog = pd.read_csv("timelog.csv")
master = pd.read_csv("gwtable.csv")
valids = pd.read_csv("fixTicktotal.csv")


def getCount(df):
    '''
    Counts the number of jobs by month and ticker
    Input: DataFrame 
    Output: List
    '''
    months = ['01','02','03','04','05','06','07','08','09','10','11','12','13']
    years = ['2016','2017','2018','2019','2020']
    countlist = []

    for i in range(5):
        if i == 0:
            for j in range(9):
                t = df[(df['post_date']< years[i]+'-'+months[j+1+3]) & (df['remove_date'] > years[i]+'-'+months[j+3])].groupby(['fixticker']).size()
                countlist.append(t)
        else:
            for j in range(12):
                if i == 4:
                    t = df[(df['post_date']< years[i]+'-'+months[1]) & (df['remove_date'] > years[i]+'-'+months[0])].groupby(['fixticker']).size()
                    countlist.append(t)
                    break
                else:
                    t = df[(df['post_date']< years[i]+'-'+months[j+1]) & (df['remove_date'] > years[i]+'-'+months[j])].groupby(['fixticker']).size()
                    
                    countlist.append(t)
                    
    return countlist
    
def blankdf(ticks):
    '''
    Creates lists for blank dataframe in desired format for modeling without key variable based on tickers
    Input: List of tickers
    Output: Lists of tickers by available months and years in dataset 

    '''
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    years = ['2016','2017','2018','2019','2020']
    monthlist = []
    yearlist = []
    tlist = []
    
    for t in ticks:
        for i in range(5):
            if i == 0:
                for j in range(9):
                    monthlist.append(months[j+3])
                    yearlist.append(years[i])
                    tlist.append(t)
            else:
                for j in range(12):
                    if i == 4:
                        monthlist.append('01')
                        yearlist.append('2020')
                        tlist.append(t)
                        break
                    else:
                        monthlist.append(months[j])
                        tlist.append(t)
                    yearlist.append(years[i])
            
    return tlist, monthlist, yearlist

def countBytick(clist,ticks):
    '''
    Creates list of job counts for entire dataframe, including zeroes
    Inputs: clist, List of counts by ticker and date
            ticks, List of available tickers in dataset
    Output: List of counts for job postings for each ticker in each available month
    '''
    
    counts = []
    
    for t in ticks:
        for i in range(46):
            if t in clist[i]:
                counts.append(clist[i][t])
            else:
                counts.append(0)
                        
    return counts

def getPercent(row):
    '''
    Given row of dataframe, calculate percent change based on counts
    Input: Dataframe row
    Output: float value of calculated weight
    '''
    if row['Ticker']==row['ticker2']:
        if row['count2']==0:
            weight = (float(row['count']) + 1) / (float(row['count2']) + 1) -1
            weight = weight*100
        else:
            weight = (float(row['count'])-float(row['count2']))/float(row['count2'])
            weight = weight*100
    else:
        weight = 0
    return weight


##############################
#Intern/Trainee Roles Section#
##############################

#Use Regular Expression to get job_ids that match desired jobs
traineetitles = titles[(titles['title'].str.contains('Train|train', na=False))]
notTrainee = titles[titles['title'].str.contains('Sr.|trainer|Trainer|Coach|Dog|Strain|Instructor|Advisor|Developer|Superintendent|Coordinator|Powertrain|Director|Supervisor|Specialist|Lead|trained|Trained|Senior|Trainer|Manage|manage|driver|Driver', na=False)]

notTitle = notTrainee[['job_id']]
traineetags = tags[(tags['tag'].str.contains('Trainee|Intern|Internship', na=False))]
notTag = tags[(tags['tag'].str.contains('International|Internal|Internet', na=False))]

Tags = traineetags[~traineetags.isin(notTag)].dropna()

Tags['job_id'] = Tags['job_id'].astype(int)

#Merge files together based on selected jobs
tagid = Tags[['job_id']]
titleid = traineetitles[['job_id']]
master2 = master[['job_id']]
time2 = timelog[['job_id','post_date','remove_date']]

tagtitle2 = pd.concat([tagid,titleid]).drop_duplicates()
tagtitle2 = tagtitle2[~tagtitle2.isin(notTitle)].dropna()
tagtitle2['job_id'] = tagtitle2['job_id'].astype(int)
val2 = valids[['job_id','fixticker']]

final = master2.merge(time2,how='inner',on='job_id')
final = final.merge(tagtitle2,how='inner',on='job_id')
final = final.merge(val2,how='inner',on='job_id')

#Ensure we are removing potential COVID-19 data
final2 = final[final['post_date']<'2020-02-01'].sort_values(by=['post_date'])


#Get job counts
clist = getCount(final2)

#Blank lists for dataframe
tlist, mlist, ylist = blankdf(uticks)

#get full list of counts including 0s
counts = countBytick(clist,uticks)

data = {
    
    'Ticker': tlist,
    'year':ylist,
    'month':mlist,
    'count':counts
     
}

#Create dataframe
df = pd.DataFrame(data)

#Create shifted columns to calculate percent change
df['count2']=df['count'].shift(1)
df['ticker2']=df['Ticker'].shift(1)

#Calculate percent change
df['weight_Intern'] = df.apply(getPercent,axis=1)

df = df[['Ticker','year','month','weight_Intern','count']]
#Export csv
df.to_csv("gw_intern2.csv",index=False)

############################
# Important Roles Section #
############################


#Use Regular Expression to get job_ids that match desired jobs
imptitles = titles[(titles['title'].str.contains("Superintendent|Admin|Supervisor|VP|Director|Officer|Chief|Sr|Exec|CEO|President|Board|Senior",na=False))]
notImptit = titles[titles['title'].str.contains('Manage|manage|driver|Driver', na=False)]

imptags = tags[(tags['tag'].str.contains('Year', na=False))]
notImptag = tags[(tags['tag'].str.contains('Round|One Year|Two Year|Five Year|1 Year|2 Year|3 Year|5 Year', na=False))]
impTags = imptags[~imptags.isin(notImptag)].dropna()
impTags['job_id'] = impTags['job_id'].astype(int)

impidTag = impTags[['job_id']]
impidTit = imptitles[['job_id']]

impidTagTit = pd.concat([impidTag,impidTit]).drop_duplicates()
notImpTit = notImptit[['job_id']]

impidTagTit = impidTagTit[~impidTagTit.isin(notTitle)].dropna()
impidTagTit['job_id'] = impidTagTit['job_id'].astype(int)


#Merge files together based on selected jobs
master2 = master[['job_id']]
time2 = timelog[['job_id','post_date','remove_date']]
val2 = valids[['job_id','fixticker']]

final = master2.merge(time2,how='inner',on='job_id')
final = final.merge(impidTagTit,how='inner',on='job_id')
final = final.merge(val2,how='inner',on='job_id')

#Ensure we are removing potential COVID-19 data
final2 = final[final['post_date']<'2020-02-01'].sort_values(by=['post_date'])

uticks = valids.fixticker.unique()
#Get job counts
clist = getCount(final2)

#Get blank lists for dataframe
tlist, mlist, ylist = blankdf(uticks)

#get job counts including 0s for each month and ticker
counts = countBytick(clist,uticks)

data = {
    
    'Ticker': tlist,
    'year':ylist,
    'month':mlist,
    'count':counts
     
}
df = pd.DataFrame(data)

#Create shifted columns to calculate percent change
df['count2']=df['count'].shift(1)
df['ticker2']=df['Ticker'].shift(1)

#Calculate percent change
df['weight_Important'] = df.apply(getPercent,axis=1)

df = df[['Ticker','year','month','weight_Important','count']]

#Export csv
df.to_csv("gw_important2.csv",index=False)
 
