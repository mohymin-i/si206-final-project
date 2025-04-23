#!/usr/bin/env bash

departures=("DTW" "ATL")
arrivals=("ORD" "NYC" "LAX" "SFO" "SJC" "DAL" "MCO" "BOS" "AUS" "LAS" "SEA")
dates=("2025-04-27" "2025-04-23" "2025-04-24" "2025-04-25" "2025-04-26")

# departures=("DTW" "ATL")
# arrivals=("ORD" "NYC")
# dates=("2025-04-25" "2025-04-26")

for dep in "${departures[@]}"; do
  for arr in "${arrivals[@]}"; do
    for date in "${dates[@]}"; do
      python ../flights/store_flights.py "$dep" "$arr" "$date"
      echo "Ran store_flights.py $dep $arr $date"
    done
  done
done
