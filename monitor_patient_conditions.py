import random
import time

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

while True:
    bp, o2 = get_patient_conditions()
    print(f"Blood Pressure: {bp}, Oxygen Level: {o2}")

    if bp > BP_THRESHOLD:
        send_alert("High blood pressure detected!")
    if o2 < O2_THRESHOLD:
        send_alert("Low oxygen level detected!")

    time.sleep(5)
