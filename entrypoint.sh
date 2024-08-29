#!/bin/sh

CHECK_INTERVAL_SECONDS=${CHECK_INTERVAL_SECONDS:-300}

# python /app/main.py

while true; do
  python /app/main.py
  sleep $CHECK_INTERVAL_SECCONDS
done
