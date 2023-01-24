import python_weather
import asyncio
import os
import matplotlib.pyplot as plt
import sys

if len(sys.argv) > 1:
  city_name = sys.argv[1]
else:
  city_name = "Columbus, OH"

async def getweather():
  days = []
  labels = []
  # declare the client. format defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(format=python_weather.IMPERIAL) as client:

    # fetch a weather forecast from a city
    weather = await client.get(city_name)
  
    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)
  
    # get the weather forecast for a few days
    for forecast in weather.forecasts:
      print(forecast.date, forecast.astronomy)
      labels.append(forecast.date)
      day = []
      # hourly forecasts
      for hourly in forecast.hourly:
        #print(f' --> {hourly!r}')
        day.append((str(hourly.time), hourly.temperature))
      days.append(day)
  return days, labels

async def main():
  days, labels = await getweather()
  for i, day in enumerate(days):
    l = [h[0] for h in day]
    r = [h[1] for h in day]
    plt.plot(l, r, '.-', label=labels[i])
  plt.title('Weather in ' + city_name + '!')
  plt.xlabel('Time')
  plt.ylabel('ºF')
  plt.legend()
  plt.show()

asyncio.run(main())
