import urllib.request
import json
from datetime import date
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
import requests
 
contents = urllib.request.urlopen("http://api.ouraring.com/v1/userinfo?access_token=N552QLEV3IPVRJ5OOP34S3NEVHYS2KRL").read()
userinfo = json.loads(contents)
print(userinfo['age'])
print(userinfo['weight'])
 
# Yesterday date
day2 = date.today() - timedelta(days = 1)
# Day befores date
day1 = date.today() - timedelta(days = 2)
print(day1)
print(day2)
#?start={day1}&end={day2}



url = 'https://api.ouraring.com/v1/sleep' 
params={ 
    'start_date': '2022-09-25', 
    'end_date': '2022-11-25' 
}
headers = { 
  'access_token': 'N552QLEV3IPVRJ5OOP34S3NEVHYS2KRL' 
}
response = requests.request('GET', url, headers=headers, params=params) 
print(response.text)
print(response.status_code)
quit()

sleep = urllib.request.urlopen(f"http://api.ouraring.com/v1/sleep?access_token=N552QLEV3IPVRJ5OOP34S3NEVHYS2KRL").read()
sleep = json.loads(sleep)

#sleepdf = pd.DataFrame(sleep.items())
full_df = pd.DataFrame.from_dict(sleep['sleep'])
#sleepdf.to_csv("sleep.csv")

#plt.plot(sleep_df["summary_date"], sleep_df.loc[['2022-11-25'],["rmssd_5min"]])
#plt.show()

#list = [0, 0, 62, 0, 75, 52, 56, 56, 64, 57, 55, 78, 77, 83, 70, 35, 21, 25, 49, 44, 48, 48, 62, 69, 66, 64, 79, 59, 67, 66, 70, 63, 53, 57, 53, 57, 38, 26, 18, 24, 30, 35, 36, 46, 53, 59, 50, 50, 53, 53, 57, 52, 41, 37, 49, 47, 48, 35, 32, 34, 52, 57, 62, 57, 70, 81, 81, 65, 69, 72, 64, 0]
#print(len(list))

full_df['datetime'] = pd.to_datetime(full_df['bedtime_end'], utc=True).dt.normalize()
full_df['weekday'] = full_df['datetime'].dt.dayofweek
full_df['weekend'] = full_df['datetime'].dt.dayofweek > 4
full_df['datetime_naive'] = full_df['datetime'].apply(lambda t: t.replace(tzinfo=None))
full_df = full_df.set_index('datetime_naive')
full_df.info()
full_df['weekend']

def plot_field(df, field_name, field_label):
    plt.rcParams["figure.figsize"] = (20,3)
    fig, ax = plt.subplots()
    plt.bar(df.index.values, field_name, data=df, axes=ax) 
    #plt.bar('datetime', field_name, data=df, axes=ax) 
    dfmt = DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(dfmt)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.set_ylabel(field_label)
    plt.xticks(rotation=90) 
    plt.show()

full_df['duration_hours']=full_df['duration']/3600 # Convert seconds to hours
full_df['deep_hours']=full_df['deep']/3600 # Convert seconds to hours

plot_field(full_df,'temperature_delta','Temperature Variation')





import json
import os

from datetime import date, timedelta
from oura import OuraClient
from dotenv import load_dotenv

load_dotenv()

oura_token = os.getenv('OURA_TOKEN')
oura_client = OuraClient(personal_access_token=oura_token)

who_am_i = oura_client.user_info()

week_past = str(date.today() - timedelta(days=7)) 
sleep_summary = oura_client.sleep_summary(start=week_past)
print (sleep_summary)

with open('result.json', 'w') as fp:
    json.dump(sleep_summary, fp, indent=4)
