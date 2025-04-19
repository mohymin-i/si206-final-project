#!/usr/bin/env bash

departures=("DTW" "ATL")
arrivals=("ORD" "NYC" "LAX" "SFO" "SJC" "DAL" "MCO" "BOS" "AUS" "LAS" "SEA")
dates=("2025-04-20" "2025-04-21" "2025-04-22" "2025-04-23" "2025-04-24")

for dep in "${departures[@]}"; do
  for arr in "${arrivals[@]}"; do
    for date in "${dates[@]}"; do
      python get_flights.py "$dep" "$arr" "$date"
      echo "Ran get_flights.py $dep $arr $date"
      python store_flights.py
      echo "Stored get_flights.py $dep $arr $date"
    done
  done
done
