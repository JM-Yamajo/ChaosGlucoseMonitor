#include <Wire.h>  // Include Wire library for I2C communication
#include "MAX30105.h"  // Include the MAX30105 library for the PPG sensor

MAX30105 ppgSensor;  // Create an instance of the MAX30105 sensor class

hw_timer_t * timerECG = NULL;  // Initialize a hardware timer for ECG
hw_timer_t * timerPPG = NULL;  // Initialize a hardware timer for PPG

portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;  // Initialize a mutex for timer

volatile bool sampleECG = false;  // Flag to indicate when to sample ECG
volatile bool samplePPG = false;  // Flag to indicate when to sample PPG

const int samplingPeriod = 5; // Sampling period in milliseconds (5ms -> 200Hz)
const unsigned long samplingDuration = 90000; // Sampling duration in milliseconds (90,000ms -> 3 minutes)
unsigned long startTime = 0;  // Variable to store the start time of sampling

enum State {
  WAITING,         // State indicating waiting for command
  SAMPLING_ECG,    // State indicating ECG sampling is in progress
  SAMPLING_PPG     // State indicating PPG sampling is in progress
};

State currentState = WAITING;  // Initialize the current state to WAITING

void IRAM_ATTR onTimerECG() {
  // Interrupt service routine for ECG timer
  portENTER_CRITICAL_ISR(&timerMux);
  sampleECG = true;  // Set ECG sample flag
  portEXIT_CRITICAL_ISR(&timerMux);
}

void IRAM_ATTR onTimerPPG() {
  // Interrupt service routine for PPG timer
  portENTER_CRITICAL_ISR(&timerMux);
  samplePPG = true;  // Set PPG sample flag
  portEXIT_CRITICAL_ISR(&timerMux);
}

void setup() {
  Serial.begin(115200);  // Start serial communication at 115200 baud

  pinMode(26, INPUT);  // Set pin 26 as input (LO+ detection)
  pinMode(27, INPUT);  // Set pin 27 as input (LO- detection)
  
  ppgSensor.begin(Wire, I2C_SPEED_FAST);  // Initialize the PPG sensor with fast I2C speed
  ppgSensor.setup();  // Set up the PPG sensor

  // Configure ECG and PPG timers
  timerECG = timerBegin(0, 80, true);
  timerPPG = timerBegin(1, 80, true);
  
  // Attach interrupts and set sampling periods for ECG and PPG timers
  timerAttachInterrupt(timerECG, &onTimerECG, true);
  timerAttachInterrupt(timerPPG, &onTimerPPG, true);
  timerAlarmWrite(timerECG, samplingPeriod * 1000, true);
  timerAlarmWrite(timerPPG, samplingPeriod * 1000, true);
}

void loop() {
  // Main loop handling different states
  if (currentState == WAITING) {
    // Waiting state checks for serial input to start ECG/PPG sampling
    if (Serial.available() > 0) {
        String sensor = Serial.readStringUntil('\n');  // Read the sensor type from serial

        if (sensor == "ECG") {
            startTime = millis();  // Record start time
            currentState = SAMPLING_ECG;  // Change state to ECG sampling
            timerAlarmEnable(timerECG);  // Enable ECG timer
        } else if (sensor == "PPG") {
            startTime = millis();  // Record start time
            currentState = SAMPLING_PPG;  // Change state to PPG sampling
            timerAlarmEnable(timerPPG);  // Enable PPG timer
        }
    }
  } else if (currentState == SAMPLING_ECG) {
    // ECG sampling state
    unsigned long currentTime = millis();
    unsigned long dt = currentTime - startTime;  // Calculate elapsed time

    if (dt >= samplingDuration) {
        timerAlarmDisable(timerECG);  // Disable ECG timer after sampling duration
        currentState = WAITING;  // Change state to waiting
    } else if (sampleECG) {
        // Sample ECG data
        portENTER_CRITICAL(&timerMux);
        sampleECG = false;
        portEXIT_CRITICAL(&timerMux);

        int ecg_value = analogRead(14);  // Read ECG value from analog pin

        Serial.print(dt);
        Serial.print(",");
        Serial.print(ecg_value);
        Serial.println();
    }
  } else if (currentState == SAMPLING_PPG) {
    // PPG sampling state
    unsigned long currentTime = millis();
    unsigned long dt = currentTime - startTime;  // Calculate elapsed time

    if (dt >= samplingDuration) {
        timerAlarmDisable(timerPPG);  // Disable PPG timer after sampling duration
        currentState = WAITING;  // Change state to waiting
    } else if (samplePPG) {
        // Sample PPG data
        portENTER_CRITICAL(&timerMux);
        samplePPG = false;
        portEXIT_CRITICAL(&timerMux);

        int ppg_value = ppgSensor.getIR();  // Read PPG value using MAX30105 sensor

        Serial.print(dt);
        Serial.print(",");
        Serial.print(ppg_value);
        Serial.println();
    }
  }
}
