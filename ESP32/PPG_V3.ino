#include <Wire.h>
#include "MAX30105.h"

MAX30105 ppgSensor;

hw_timer_t * timerECG = NULL;
hw_timer_t * timerPPG = NULL;

portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

volatile bool sampleECG = false;
volatile bool samplePPG = false;

const int samplingPeriod = 5; // 5 ms corresponde a 200 Hz
const unsigned long samplingDuration = 90000; // Duración del muestreo: 3 minutos en ms
unsigned long startTime = 0;

enum State {
  WAITING,
  SAMPLING_ECG,
  SAMPLING_PPG
};

State currentState = WAITING;

void IRAM_ATTR onTimerECG() {
  
  portENTER_CRITICAL_ISR(&timerMux);
  sampleECG = true;
  portEXIT_CRITICAL_ISR(&timerMux);
}

void IRAM_ATTR onTimerPPG() {

  portENTER_CRITICAL_ISR(&timerMux);
  samplePPG = true;
  portEXIT_CRITICAL_ISR(&timerMux);

}

void setup() {

  Serial.begin(115200);

  pinMode(26, INPUT); // Configuración para la detección LO +
  pinMode(27, INPUT); // Configuración para la detección LO -
  
  ppgSensor.begin(Wire, I2C_SPEED_FAST);
  ppgSensor.setup();

  timerECG = timerBegin(0, 80, true);
  timerPPG = timerBegin(1, 80, true);
  
  timerAttachInterrupt(timerECG, &onTimerECG, true);
  timerAttachInterrupt(timerPPG, &onTimerPPG, true);
  timerAlarmWrite(timerECG, samplingPeriod * 1000, true);
  timerAlarmWrite(timerPPG, samplingPeriod * 1000, true);

}

void loop() {

  if (currentState == WAITING) {

    if (Serial.available() > 0) {
        String sensor = Serial.readStringUntil('\n');

        if (sensor == "ECG") {

            startTime = millis();
            currentState = SAMPLING_ECG;
            timerAlarmEnable(timerECG);

        } else if (sensor == "PPG") {

            startTime = millis();
            currentState = SAMPLING_PPG;
            timerAlarmEnable(timerPPG);

        }

    }

  } else if (currentState == SAMPLING_ECG) {

    unsigned long currentTime = millis();
    unsigned long dt = currentTime - startTime;

    if (dt >= samplingDuration) {

        timerAlarmDisable(timerECG);
        //Serial.println("Muestreo completado para ECG");
        currentState = WAITING;

    } else if (sampleECG) {

        portENTER_CRITICAL(&timerMux);
        sampleECG = false;
        portEXIT_CRITICAL(&timerMux);

        int ecg_value = analogRead(14);

        Serial.print(dt);
        Serial.print(",");
        Serial.print(ecg_value);
        Serial.println();
        //delay(20);

    }

  } else if (currentState == SAMPLING_PPG) {

    unsigned long currentTime = millis();
    unsigned long dt = currentTime - startTime;

    if (dt >= samplingDuration) {

        timerAlarmDisable(timerPPG);
        //Serial.println("Muestreo completado para PPG");
        currentState = WAITING;

    } else if (samplePPG) {

        portENTER_CRITICAL(&timerMux);
        samplePPG = false;
        portEXIT_CRITICAL(&timerMux);

        int ppg_value = ppgSensor.getIR();

        Serial.print(dt);
        Serial.print(",");
        Serial.print(ppg_value);
        Serial.println();

    }

  }

}
