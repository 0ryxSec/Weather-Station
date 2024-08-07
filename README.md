# Weather-Station

Python Script for sense hat that runs on raspberry pi.

1  -  It takes the temperature, humidity and pressure every second, records it to a file (sensor_data_log.csv)

2  -  It takes an average temperature based off the previous 60 readings, determines the trend, and then colors the sense hat's LEDs according to the below format:

Red - Temperature is rising, this triggers when the average temperature is rising.
Blue - Temperature is dropping, this triggers when the average temperature is falling.
Green  -  Temperature is stable.

3  -  The current temperature will also display on the LEDs in White.



USAGE:
python3 weather-station.py
