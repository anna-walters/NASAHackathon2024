import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sunrise_sunset import data
import urllib
import urllib.request
import ast 
import datetime as dt
import meteomatics.api as api


def east_or_west(df,noon):
    def filter_by_day(df, day):
        day_df = df[df["TMSTAMP"].dt.date == pd.to_datetime(day).date()].copy()
    
        #max_elevation = pd.to_datetime(str(day)+' '+str(solar_max_time)[:-3])


        conditions = [
            (day_df["TMSTAMP"] <= noon),
            (day_df["TMSTAMP"] > noon)
        ]

        choices = ["east", "west"]

        day_df["direction"] = np.select(conditions, choices, default="NaN")
        
        return day_df
    
    all_days_df = pd.DataFrame()
    for day in df["TMSTAMP"].dt.date.unique():
         this_day_df = filter_by_day(df,day)
         all_days_df = pd.concat([all_days_df,this_day_df])
    
    return all_days_df

def get_solar_noon(date = "2024-02-22"):
    
    url_base = "https://api.sunrise-sunset.org/json?"
    lat = 50.576710 # Example Lat 
    long = -3.811770 # Example Long 

    test = urllib.request.urlopen("https://api.sunrise-sunset.org/json?lat=50.576710&lng=-3.811770&date="+date)

    data = ast.literal_eval(test.read().decode())

    return data["results"]["solar_noon"]

def get_solar_elevation(choice = dt.datetime(2024, 2, 22, 0, 0), coordinates_ts = [(50.5766888,-3.8117336)]):
    startdate_ts = choice
    enddate_ts = startdate_ts + dt.timedelta(days=1)
    interval_ts = dt.timedelta(minutes=1)
    parameters_ts = ['uv:idx', 'sun_elevation:d', 'sun_azimuth:d']
    
    username = "carr_luke"
    password = "50Aq99CDfu"

    try:
        df_ts = api.query_time_series(coordinates_ts, startdate_ts, enddate_ts, interval_ts,
                                    parameters_ts, username, password)
        df_ts["TMSTAMP"] = pd.date_range(startdate_ts, enddate_ts, freq='min')


    except Exception as e:
        print("Failed, the exception is {}".format(e))
    
    return df_ts
    


def main():
    choice = input("What date would you like to get the solar elevation for? (YYYY-MM-DD)")

    s_noon = get_solar_noon(choice)
    choice_noon = pd.to_datetime(choice +' ' + s_noon)
    choice = dt.datetime.strptime(choice, "%Y-%m-%d")

    df = get_solar_elevation(choice)
    df = df.rename(columns={"sun_elevation:d": "Solar Elevation", "sun_azimuth:d": "Solar Azimuth"})

    df = east_or_west(df,choice_noon)
    df = df[df["Solar Elevation"] > 0]
    
    df.set_index("TMSTAMP", inplace=True)

    df = df[["Solar Elevation", "Solar Azimuth"]].resample('1h').mean()
    df["Solar Elevation"] = df["Solar Elevation"].round()
    df["Solar Azimuth"] = df["Solar Azimuth"].round()
    print(df)

    
        
main()