# v0.3 07/08/2024


from sense_hat import SenseHat
from datetime import datetime
import time
import csv
import os

# Initialize Sense HAT
sense = SenseHat()

# Path to your sensor data log file
log_file_path = os.path.expanduser('~/weather/sensor_data_log.csv')

# Create the log file if it doesn't exist and write the header
if not os.path.isfile(log_file_path):
    with open(log_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'temperature', 'humidity', 'pressure'])

# Function to get color based on temperature trend
def get_trend_color(recent_readings):
    if len(recent_readings) < 2:
        return (255, 255, 255)  # White if not enough data

    if recent_readings[-1] > recent_readings[0]:
        return (255, 0, 0)  # Red for rising temperature
    elif recent_readings[-1] < recent_readings[0]:
        return (0, 0, 255)  # Blue for falling temperature
    else:
        return (0, 255, 0)  # Green for stable temperature

# Function to set the LED rotation based on gyroscope data
def set_led_rotation():
    orientation = sense.get_orientation_degrees()
    pitch = orientation['pitch']
    roll = orientation['roll']

    if 45 <= pitch < 135:
        sense.set_rotation(90)
    elif 135 <= pitch < 225:
        sense.set_rotation(180)
    elif 225 <= pitch < 315:
        sense.set_rotation(270)
    else:
        sense.set_rotation(0)

# Initialize a list to store temperature readings for the last minute
minute_readings = []

while True:
    # Get current timestamp and sensor data, this is rounded to 2 decimal places
    current_time = datetime.now().replace(microsecond=0)
    current_temp = round(sense.get_temperature(), 2)
    current_humidity = round(sense.get_humidity(), 2)
    current_pressure = round(sense.get_pressure(), 2)

    # Add the current temperature reading to the minute_readings list
    minute_readings.append(current_temp)

    # If we have more than 60 readings, remove the oldest one
    if len(minute_readings) > 60:
        minute_readings.pop(0)

    # Record the sensor data to the log file
    with open(log_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, current_temp, current_humidity, current_pressure])

    # Print the sensor data to the console
    print(f"Time: {current_time}, Temp: {current_temp:.2f}C, Humidity: {current_humidity:.2f}%, Pressure: {current_pressure:.2f}hPa")

    # Every minute, calculate the average temperature and determine the trend
    if len(minute_readings) == 60:
        avg_temp = round(sum(minute_readings) / len(minute_readings), 2)
        trend_color = get_trend_color(minute_readings)

        # Light up the Sense HAT with the trend color
        sense.clear(trend_color)

        # Set the LED rotation based on gyroscope data
        set_led_rotation()

        # Display the average temperature on the Sense HAT LED
        sense.show_message(f"{avg_temp:.2f}C", text_colour=[255, 255, 255], back_colour=trend_color)

    # Wait for a second before taking the next reading
    time.sleep(1)
