import cv2
import numpy as np
from datetime import datetime
from imutils.video import VideoStream
import random
import time
import threading

# Load YOLO
net = cv2.dnn.readNet("yolo/yolov3-custom.weights", "yolo/yolov3-custom.cfg")
with open("yolo/obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Initialize video stream
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Define thresholds for emergency conditions
BP_THRESHOLD = 140  # Example threshold for blood pressure
O2_THRESHOLD = 90   # Example threshold for oxygen level

# Simulate patient condition data
def get_patient_conditions():
    bp = random.randint(80, 160)
    o2 = random.randint(85, 100)
    return bp, o2

# Function to send alerts
def send_alert(message):
    print(f"ALERT: {message}")

# Function to monitor patient conditions
def monitor_patient_conditions():
    while True:
        bp, o2 = get_patient_conditions()
        print(f"Blood Pressure: {bp}, Oxygen Level: {o2}")

        if bp > BP_THRESHOLD:
            send_alert("High blood pressure detected!")
        if o2 < O2_THRESHOLD:
            send_alert("Low oxygen level detected!")

        time.sleep(5)

# Start patient monitoring in a separate thread
threading.Thread(target=monitor_patient_conditions, daemon=True).start()

# Real-time person detection loop
while True:
    frame = vs.read()
    frame = cv2.resize(frame, (640, 480))

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] in ["person"]:  # Only detect persons
                center_x = int(detection[0] * 640)
                center_y = int(detection[1] * 480)
                w = int(detection[2] * 640)
                h = int(detection[3] * 480)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indices:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Note time of entry
            entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{label} detected at {entry_time}")

    cv2.imshow('TeleICU Monitoring', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
vs.stop()
