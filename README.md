# ChaosGlucoseMonitor

## Overview
This project leverages chaos theory to analyze biosignals for non-invasive blood glucose monitoring. It focuses on utilizing electrocardiographic (ECG) and photoplethysmography (PPG) signals with an ESP32 microcontroller and an MAX30105 sensor.

## Key Features
- Acquisition of ECG and PPG signals using ESP32.
- Application of chaos theory principles for biosignal analysis.
- Non-invasive methodology for monitoring blood glucose levels.

## Hardware Requirements
- ESP32 microcontroller
- MAX30105 sensor for PPG signal acquisition

## Software Requirements
- Arduino IDE for programming the ESP32
- Python for data analysis and visualization
- Required Python Libraries: `numpy`, `pandas`, `matplotlib`, `sklearn`, `scipy`, `ipython`

## Setup and Installation
1. Assemble the hardware setup with the ESP32 and MAX30105.
2. Upload the `PPG_v3.ino` sketch to the ESP32 for ECG and PPG data acquisition.
3. Execute the `Serial_V4.ipynb` Jupyter Notebook for initial data processing.
4. Run the `atractor_v10.py` Python script for advanced data analysis and visualization.

## Script Descriptions
- **`PPG_v3.ino`**: Arduino sketch responsible for collecting PPG and ECG signals using the ESP32 and storing them for further analysis.
- **`Serial_V4.ipynb`**: Jupyter Notebook for processing the raw signals collected by the ESP32, preparing the data for chaos theory analysis.
- **`atractor_v10.py`**: Python script applying chaos theory techniques to the processed signals, including phase space reconstruction and other advanced analytical methods.

## Data Collection
- Data is collected from ECG and PPG sensors and stored for subsequent analysis.
- The system supports real-time data collection and storage.

## Analysis Techniques
- Utilizes techniques such as mutual information calculation, embedding dimension estimation, and phase space reconstruction.
- Python scripts for each analytical technique are provided, with detailed comments.

## Contributing
Contributions are welcome. Please fork the repository and submit pull requests for review.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
Special thanks to all contributors and researchers in the field of chaos theory and biosignal analysis.
