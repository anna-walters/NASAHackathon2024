import pandas as pd
import numpy as np
import matplotlib.pyplot

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

def hackathon():
    now = datetime.datetime.now()
    start = datetime.datetime(2024, 1, 1)
    minutes = pd.date_range(start, now, freq='T')
    df = pd.DataFrame({'TMSTAMP': minutes})
    print(df)
    
    aoe_list = []
    st_list = []

    for entry in df["TMSTAMP"]:
        res = calc_aoe(entry)
        aoe_list.append(res[0])
        st_list.append(res[1])

    df["Solar Elevation"] = aoe_list
    df = df[df["TMSTAMP"] == pd.to_datetime("2024-02-03 7:00:00")]
    print(df)
    plt.plot(df["TMSTAMP"], df["Solar Elevation"])
    plt.show()
    print(df)