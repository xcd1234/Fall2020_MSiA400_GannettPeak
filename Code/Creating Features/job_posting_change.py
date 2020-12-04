import pandas as pd
import csv
from datetime import datetime
import statistics

# create empty dictionary with month as keys, given first and last month, make a key for all months in between, and initialize value to 0
def date_list(first, last):
    result = {}
    first_year = int(first[:4])
    first_month = int(first[5:])
    last_year = int(last[:4])
    last_month = int(last[5:])
    while first_year != last_year or first_month != last_month:
        date = str(first_year).zfill(2) + "-" + str(first_month).zfill(2)
        result[date] = 0
        if first_month < 12:
            first_month += 1
        else:
            first_month = 1
            first_year += 1
    last_date = str(last_year).zfill(2) + "-" + str(last_month).zfill(2)
    result[last_date] = 0
    return result

# count active job postings for each company for each month given a dictionary
def month_count(dic, start, end):
    start_year = int(start[:4])
    start_month = int(start[5:])
    end_year = int(end[:4])
    end_month = int(end[5:])
    while start_year != end_year or start_month != end_month:
        date = str(start_year).zfill(2) + "-" + str(start_month).zfill(2)
        dic[date] += 1
        if start_month < 12:
            start_month += 1
        else:
            start_month = 1
            start_year += 1
    end_date = str(end_year).zfill(2) + "-" + str(end_month).zfill(2)
    dic[end_date] += 1

df1 = pd.read_csv("ticker_first_last.csv")
result1 = {}
result2 = {}
for index, row in df1.iterrows():
    ticker = row['ticker']
    first = row['first']
    last = row['last']
    result1[ticker] = date_list(first, last)
    result2[ticker] = date_list(first, last)

df2 = pd.read_csv("ticker_id_start_end.csv")
for index, row in df2.iterrows():
    ticker = row['ticker']
    start = row['startmonth']
    end = row['endmonth']
    if start <= end:
        month_count(result1[ticker], start, end)

# calculate change in percentage of active job postings from month to month for each company
def add_percentage(dic):
    count = 0
    result = []
    tickers = dic.keys()
    for ticker in tickers:
        month_counts = dic[ticker]
        months = list(month_counts.keys())
        for i in range(1, len(months)):
            temp = []
            current = month_counts[months[i]]
            previous = month_counts[months[i-1]]
            if previous != 0:
                change = current * 1.0 / previous - 1
            else:
                change = (current + 1) * 1.0 / (previous + 1) - 1
                count += 1
            temp.append(ticker)
            temp.append(months[i])
            temp.append(change)
            result.append(temp)
    print(count)
    return result

percentages = add_percentage(result1)

with open("output1.csv", 'w') as f1:
    writer = csv.writer(f1, lineterminator='\n')
    writer.writerow(["ticker", "month", "job posting change"])
    writer.writerows(percentages)

df3 = pd.read_csv("ticker_id_post_remove.csv")

# get the last day of the month given year and month
def last_day_of_month(yearmonth):
    year = yearmonth[:4]
    month = yearmonth[5:]
    if month in ['01', '03', '05', '07', '08', '10', '12']:
        return yearmonth + '-31'
    elif month in ['04', '06', '09', '11']:
        return yearmonth + '-30'
    else:
        if int(year) % 4 == 0:
            return yearmonth + '-29'
        else:
            return yearmonth + '-28'

# get the number of days in a month given year and month
def month_day(yearmonth):
    year = yearmonth[:4]
    month = yearmonth[5:]
    if month in ['01', '03', '05', '07', '08', '10', '12']:
        return 31
    elif month in ['04', '06', '09', '11']:
        return 30
    else:
        if int(year) % 4 == 0:
            return 29
        else:
            return 28

for ticker in result2.keys():
    for month in result2[ticker].keys():
        result2[ticker][month] = []

for index, row in df3.iterrows():
    ticker = row['ticker']
    post = row['post_date']
    remove = row['remove_date']
    durations = date_list(post[:7], remove[:7])
    yearmonths = list(durations.keys())
    if len(yearmonths) == 1:
        durations[post[:7]] = (datetime.strptime(remove, '%Y-%m-%d') - datetime.strptime(post, '%Y-%m-%d')).days
    else:
        for i in range(len(yearmonths)):
            month_end = last_day_of_month(yearmonths[i])
            if i == 0:
                days = (datetime.strptime(month_end, '%Y-%m-%d') - datetime.strptime(post, '%Y-%m-%d')).days
                durations[yearmonths[i]] = days
            elif i == len(yearmonths) - 1:
                days = (datetime.strptime(remove, '%Y-%m-%d') - datetime.strptime(last_day_of_month(yearmonths[i - 1]), '%Y-%m-%d')).days
                durations[yearmonths[i]] = days + durations[yearmonths[i-1]]
            else:
                days = month_day(yearmonths[i])
                durations[yearmonths[i]] = days + durations[yearmonths[i-1]]
    for key in durations.keys():
        result2[ticker][key].append(durations[key])
        
# calculate average duration for each company for each month given a dictionary
def average_duration(dic):
    result = []
    for ticker in dic.keys():
        for month in dic[ticker].keys():
            monthly_durations = dic[ticker][month]
            if len(monthly_durations) == 0:
                average = 0
            else:
                average = statistics.mean(monthly_durations)
            temp = []
            temp.append(ticker)
            temp.append(month)
            temp.append(average)
            result.append(temp)
    return result

average_durations = average_duration(result2)
with open("output2.csv", 'w') as f2:
    writer = csv.writer(f2, lineterminator='\n')
    writer.writerow(["ticker", "month", "average job posting duration"])
    writer.writerows(average_durations)