# Chaos Theory in Biosignals for Glucose Monitoring

## Overview
This project applies chaos theory to analyze biosignals for non-invasive blood glucose monitoring. It focuses on using electrocardiographic (ECG) and photoplethysmography (PPG) signals with an ESP32 microcontroller and MAX30105 sensor.

## Key Features
- ECG and PPG signal acquisition using ESP32.
- Analysis of biosignals using chaos theory principles.
- Non-invasive approach for monitoring blood glucose levels.

## Hardware Requirements
- ESP32 microcontroller.
- MAX30105 sensor for PPG signal acquisition.

## Software Requirements
- Arduino IDE for ESP32 programming.
- Python for data analysis and visualization.
- Required Python Libraries: numpy, pandas, matplotlib, sklearn, scipy, ipython.

## Setup and Installation
1. Assemble the hardware setup with ESP32 and MAX30105.
2. Upload the `PPG_v3.ino` Arduino sketch to ESP32 for ECG and PPG data acquisition.
3. Execute the `Serial_V4.ipynb` Jupyter Notebook for initial data processing.
4. Run the `atractor_v10.py` Python script for advanced data analysis and visualization.

## Scripts Description
- `PPG_v3.ino`: This Arduino sketch is responsible for collecting PPG and ECG signals using ESP32 and storing them for further analysis.
- `Serial_V4.ipynb`: A Jupyter Notebook for processing the raw signals collected by the ESP32. It prepares the data for chaos theory analysis.
- `atractor_v10.py`: This Python script applies chaos theory techniques to the processed signals, including phase space reconstruction and other advanced analytical methods.

## Data Collection
- Data is collected from ECG and PPG sensors and stored for analysis.
- The system provides real-time data collection and storage capabilities.

## Analysis Techniques
- The project uses techniques such as mutual information calculation, embedding dimension estimation, and phase space reconstruction.
- Python scripts are provided for each analytical technique, along with detailed comments.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit pull requests for review.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Special thanks to all contributors and researchers in the field of chaos theory and biosignal analysis.
