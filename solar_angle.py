import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sunrise_sunset import data
import urllib
import urllib.request
import ast 
import datetime as dt
import meteomatics.api as api




def calc_aoe(date_time, longitude=50.6, latitude=-3.8):
        """
        Args:
            longitude: float, longitude of location in degrees
            latitude: float, latitude of location in degrees
            day: int, day of year
            minute: int, minute of day
        Returns:
            ModH: float, angle of elevation of sun corrected for refraction in degrees
        """
        # Angle of Day in radians
        day = date_time.dayofyear
        minute = date_time.minute

        # day: 1 = Jan 1st. 365 = Dec 31st. Assumed that Feb has 28 days.
        D = 2 * np.pi * (day - 1) / 365

        # Equation of Time
        ET = 229.18 * (
            0.000075
            + (0.001868 * np.cos(D))
            - (0.032077 * np.sin(D))
            - (0.014615 * np.cos(2 * D))
            - (0.040849 * np.sin(2 * D))
        )
        # Solar Time
        ST = date_time + pd.Timedelta(minutes=4 * (np.abs(longitude)) + ET)

        # Hour Angle in Radians
        HA = 2 * np.pi * (ST.hour * 60 + ST.minute + ST.second / 60 - 720) / 1440

        # Declination of day (degrees)
        DEC = (180 / np.pi) * (
            0.006918
            - (0.399912 * np.cos(D))
            + (0.070257 * np.sin(D))
            - (0.006758 * np.cos(2 * D))
            + (0.000907 * np.sin(2 * D))
            - (0.002697 * np.cos(3 * D))
            + (0.00148 * np.sin(3 * D))
        )
        LA = latitude

        # sine of angle of elevation of sun throughout day

        SINH = (np.sin(np.radians(LA)) * np.sin(np.radians(DEC))) + (
            np.cos(np.radians(DEC)) * np.cos(np.radians(LA)) * np.cos((HA))
        )
        # angle of elevation uncorrected for refraction
        H = np.arcsin(SINH)
        return np.degrees(H), ST

def east_or_west(df):
    def filter_by_day(df, day):
        day_df = df[df["TMSTAMP"].dt.date == pd.to_datetime(day).date()].copy()
        solar_max_elevation = day_df["Solar Elevation"].max()
        solar_max_time = get_solar_noon()
    
        max_elevation = pd.to_datetime(str(day)+' '+str(solar_max_time)[:-3])


        conditions = [
            (day_df["TMSTAMP"] <= solar_max_time),
            (day_df["TMSTAMP"] > solar_max_time)
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
    date = "2024-02-22"

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
    choice = dt.datetime.strptime(choice, "%Y-%m-%d")
    df = get_solar_elevation(choice)
    df = df.rename(columns={"sun_elevation:d": "Solar Elevation", "sun_azimuth:d": "Solar Azimuth"})
    df = east_or_west(df)
    
    print(df.head())
    print("Solar Noon: ", s_noon)
    
    
        
main()