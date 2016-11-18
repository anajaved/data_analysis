import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename = '/datasets/ud170/subway/nyc_subway_weather.csv'
subway_df = pd.read_csv(filename)
#Plots of subway ridership on both days with rain and days without rain

rain_data=subway_df.groupby(['rain', 'day_week'] , as_index=False)[['ENTRIESn_hourly']].mean()

rain= plt.plot(rain_data.iloc[0:7]['day_week'], rain_data.iloc[0:7]['ENTRIESn_hourly'], label='Rain', linestyle='--' )
no_rain=plt.plot(rain_data.iloc[7:]['day_week'], rain_data.iloc[7:]['ENTRIESn_hourly'], label='No Rain')

plt.xlabel("Days of the Week")
plt.ylabel("Entries Per Hour")
plt.legend()
plt.show(rain, no_rain)