# AI Driver Drowsiness Detection System

## Overview

This project is a real-time driver drowsiness detection system developed using Python, OpenCV, Dlib, and ESP32. It monitors the driver's eye movements through a webcam and detects signs of fatigue using Eye Aspect Ratio (EAR) and blink duration analysis. When drowsiness is detected, the system sends an HTTP request to an ESP32, which can activate an external alert device such as a buzzer or LED.

## Features

- Real-time face detection
- Facial landmark detection using Dlib
- Eye Aspect Ratio (EAR) calculation
- Blink detection and blink counting
- Average blink duration analysis
- Drowsiness detection based on eye closure and blink patterns
- ESP32 integration for hardware-based alerts
- Live monitoring using a webcam

## Technologies Used

- Python
- OpenCV
- Dlib
- NumPy
- SciPy
- Requests
- ESP32

## Download the Facial Landmark Model

This project requires the `shape_predictor_68_face_landmarks.dat` model file, which is not included in this repository due to its size.

Download it from:

http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

Extract the downloaded archive and place the `shape_predictor_68_face_landmarks.dat` file in the project root directory.

## Project Structure

```
AI-Driver-Drowsiness-Detection/
│
├── main_code.py
├── requirements.txt
├── README.md
├── shape_predictor_68_face_landmarks.dat
├── images/
│   ├── output.png
│   └── setup.png
└── ESP32_Code/
    └── esp_code.ino
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Adwaith-official/AI-Driver-Drowsiness-Detection.git
```

Navigate to the project directory:

```bash
cd AI-Driver-Drowsiness-Detection
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Download the `shape_predictor_68_face_landmarks.dat` file and place it in the project directory.

## Usage

1. Connect the ESP32 to the same network as the computer.
2. Update the ESP32 IP address in `main_code.py`.
3. Ensure the facial landmark model file is present in the project folder.
4. Run the application:

```bash
python srpfinal.py
```

The application will start the webcam, monitor the driver's eyes, and trigger an alert through the ESP32 when drowsiness is detected.

## System Workflow

1. Capture video frames from the webcam.
2. Detect the driver's face.
3. Extract facial landmarks.
4. Compute the Eye Aspect Ratio (EAR).
5. Detect eye closure and analyze blink duration.
6. Determine the driver's drowsiness state.
7. Send an alert signal to the ESP32 when necessary.

## Hardware Requirements

- ESP32 Development Board
- Webcam
- Computer or Laptop
- Optional: Buzzer or LED for alerts

## Future Improvements

- Head pose estimation
- Yawning detection
- Deep learning-based fatigue detection
- Mobile notifications
- Cloud-based monitoring and logging

## Author

J Adwaith

Electrical and Electronics Engineering Student

TKM College of Engineering

## License

This project is licensed under the MIT License.
