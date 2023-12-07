
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
