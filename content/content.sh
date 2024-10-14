#!/bin/bash

# Run the first Python script to generate anomalies and their classifications
echo "Running generate_anomaly_output.py..."
python3 classifications.py

# Check if the first script was successful
if [ $? -ne 0 ]; then
    echo "generate_anomaly_output.py failed."
    exit 1
fi

# Run the second Python script to search for light curves
echo "Running search_lightcurves.py..."
python3 lightcurveCreate.py

# Check if the second script was successful
if [ $? -ne 0 ]; then
    echo "search_lightcurves.py failed."
    exit 1
fi

./extractSectors.sh

echo "All scripts ran successfully."
