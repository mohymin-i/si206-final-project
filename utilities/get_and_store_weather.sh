#!/usr/bin/env bash

# Location codes: 348308 351409 349727 347625 347629 347936 351194

for code in 348308 351409 349727 347625 347629 347936 351194; do

  python ../weather/get_weather.py "$code" daily
  echo "Ran get_weather.py $code daily"
  python ../weather/store_weather.py daily
  echo "Stored daily weather for code $code"

  python ../weather/get_weather.py "$code" hourly
  echo "Ran get_weather.py $code hourly"
  python ../weather/store_weather.py hourly
  echo "Stored hourly weather for code $code"

done