import RPi.GPIO as GPIO
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Ultrasonic Sensor GPIO pins
TRIG_PIN = 17
ECHO_PIN = 18

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Define Google Sheets-related variables
credentials_file = 'smart-parkingiot-095b74826f5a'  # Replace with your credentials file
google_sheets_name = 'parkingdata'  # Replace with your Google Sheets document name
sheet_name = 'Sheet1'  # Replace with your sheet name

# Initialize Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
gc = gspread.authorize(credentials)
worksheet = gc.open(google_sheets_name).worksheet(sheet_name)

try:
    while True:
        # Measure distance using ultrasonic sensor
        GPIO.output(TRIG_PIN, False)
        time.sleep(2)

        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound (343 m/s)

        # Get current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Determine occupancy status based on distance threshold
        distance_threshold = 50
        occupancy_status = "Occupied" if distance < distance_threshold else "Vacant"

        # Log data to Google Sheets
        worksheet.append_row([timestamp, distance, occupancy_status])

        print(f"Timestamp: {timestamp}, Distance: {distance} cm, Occupancy: {occupancy_status}")
        time.sleep(5)  # Adjust the time interval as needed

except KeyboardInterrupt:
    GPIO.cleanup()
