######## Emergency Notification (Using Twilio API for SMS Alerts) ########
from twilio.rest import Client

def send_emergency_alert(patient_id, heart_rate, oxygen_level):
    account_sid = ' ' ##provide your account sid
    auth_token = ' ' ##provide your twilio authentication token
    client = Client(account_sid, auth_token)
    
    alert_message = f"Emergency Alert for {patient_id}! Heart Rate: {heart_rate}, Oxygen Level: {oxygen_level}."
    
    message = client.messages.create(
        body=alert_message,
        from_='+1234567890',  # provide your Twilio number
        to='+0987654321'       # Doctor phone number
    )
    
    print(f"Alert sent to doctor: {message.sid}")

# Example of sending an alert
send_emergency_alert('Patient001', 55, 88)


########  Backend with Flask for Managing Data and Alerts  #########
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/vitals', methods=['POST'])
def add_vital_record():
    data = request.json
    patient_id = data['patient_id']
    heart_rate = data['heart_rate']
    blood_pressure = data['blood_pressure']
    oxygen_level = data['oxygen_level']
    
    simulate_vitals(patient_id)  # Store in the database
    return jsonify({'status': 'Vitals Recorded'})

@app.route('/api/alert', methods=['POST'])
def alert_doctor():
    data = request.json
    patient_id = data['patient_id']
    heart_rate = data['heart_rate']
    oxygen_level = data['oxygen_level']
    
    send_emergency_alert(patient_id, heart_rate, oxygen_level)
    return jsonify({'status': 'Alert Sent'})

if __name__ == '__main__':
    app.run(debug=True)
