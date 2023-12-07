
# Glucose Monitoring System Using ESP32

## Overview
This project involves using ESP32 for non-invasive glucose monitoring by analyzing ECG and PPG signals. The Python script interacts with the ESP32 to collect and process biosignal data.

## Requirements
- Python 3
- Libraries: os, time, serial, numpy
- ESP32 microcontroller
- MAX30102 sensor

## Setup
1. Connect ESP32 to your computer.
2. Ensure the MAX30102 sensor is properly attached to ESP32.
3. Install the required Python libraries if not already installed.

## Running the Script
1. Open the script in a Python environment.
2. Modify the `port` variable in the script to match the COM port your ESP32 is connected to.
3. Run the script.
4. Follow the on-screen instructions to input user data and conduct tests.

## Data Collection
- The script collects personal data (name, age, etc.) and stores it in a private folder.
- ECG and PPG data are collected separately and stored in respective folders.

## Notes
- Ensure the ESP32 is correctly configured and the serial communication is working.
- The script saves all data in a structured folder system for easy access and analysis.

## Additional Script for Data Analysis

### Overview
This script complements the ESP32 data collection by analyzing the collected ECG and PPG signals. It includes functions for reading data, calculating auto mutual information, estimating the embedding dimension, and plotting attractors and other analytical graphs.

### Requirements
- Python libraries: os, math, nolds, numpy, matplotlib, mpl_toolkits, sklearn
- Data files in '.txt' format containing ECG or PPG data

### Running the Analysis Script
1. Ensure that the data files from the ESP32 script are stored in a structured format (preferably in 'ECG' and 'PPG' folders).
2. Run the analysis script in the same Python environment.
3. The script automatically processes data files and generates analytical plots and complexity measures.

### Key Functionalities
- Reading and plotting time series data.
- Calculating mutual information and embedding dimensions.
- Phase space reconstruction and attractor plotting.
- Estimating Lyapunov exponent, correlation dimension, and Hurst exponent for complexity analysis.

### Output
The script generates plots and saves them in a directory structure alongside the data files. It also prints out complexity measures for further analysis.
