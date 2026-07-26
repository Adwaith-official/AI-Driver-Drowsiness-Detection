import cv2
import dlib
from scipy.spatial import distance
import time
import numpy as np
import requests

# ---------------- ESP32 CONFIG ----------------
ESP32_IP = "10.230.195.42"   # change to your ESP32 IP
ALERT_ON_URL = f"http://{ESP32_IP}/alert=ON"
ALERT_OFF_URL = f"http://{ESP32_IP}/alert=OFF"

def send_alert(state):
    try:
        if state == "ON":
            requests.get(ALERT_ON_URL, timeout=0.5)
        else:
            requests.get(ALERT_OFF_URL, timeout=0.5)
    except:
        pass

# ---------------- EAR FUNCTION ----------------
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# ---------------- INITIALIZATION ----------------
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
"shape_predictor_68_face_landmarks.dat")
)

LEFT_EYE = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

cap = cv2.VideoCapture(0)

# ---------------- PARAMETERS ----------------
EAR_THRESHOLD = 0.25
BLINK_FRAMES = 3
EYE_CLOSED_TIME = 1
DROWSY_BLINK_MS = 350
WINDOW_SIZE = 15

blink_count = 0
frames = 0
eye_closed_start = None
blink_start_time = None
blink_durations = []
alarm_on = False

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in LEFT_EYE]
        right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in RIGHT_EYE]

        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

        # ---------------- EYE CLOSED ----------------
        if ear < EAR_THRESHOLD:

            frames += 1

            if blink_start_time is None:
                blink_start_time = time.time()

            if eye_closed_start is None:
                eye_closed_start = time.time()
            else:
                elapsed = time.time() - eye_closed_start

                if elapsed >= EYE_CLOSED_TIME and not alarm_on:
                    alarm_on = True
                    send_alert("ON")

        # ---------------- EYE OPEN ----------------
        else:

            if frames >= BLINK_FRAMES:
                blink_count += 1

            # Blink duration calculation
            if blink_start_time is not None:
                blink_duration = (time.time() - blink_start_time) * 1000
                blink_start_time = None

                blink_durations.append(blink_duration)

                if len(blink_durations) > WINDOW_SIZE:
                    blink_durations.pop(0)

            frames = 0
            eye_closed_start = None

            if alarm_on:
                alarm_on = False
                send_alert("OFF")

        # ---------------- AVERAGE BLINK ANALYSIS ----------------
        avg_blink = 0

        if len(blink_durations) >= WINDOW_SIZE:
            avg_blink = np.mean(blink_durations)

            if avg_blink > DROWSY_BLINK_MS and not alarm_on:
                alarm_on = True
                send_alert("ON")

        # ---------------- DISPLAY ----------------
        cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.putText(frame, f"Blinks: {blink_count}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        cv2.putText(frame, f"Avg Blink: {int(avg_blink)} ms", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        for (x, y) in left_eye + right_eye:
            cv2.circle(frame, (x, y), 2, (0,0,255), -1)

    if alarm_on:
        cv2.putText(frame, "DROWSINESS ALERT!", (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) == 27:
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()