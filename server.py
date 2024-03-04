# Import necessary modules
from flask import Flask, Response,render_template
import cv2
import logging
import time
import numpy as np
import cv2 as cv

# Create a Flask app instance
app = Flask(__name__, static_url_path='/static')

# Function to generate video frames from the camera
def generate_frames():
    camera_rtsp = cv2.VideoCapture('rtsp://192.168.144.10:8554/H264Video')
    while True:
        start_time = time.time()
        success_rtsp, frame_rtsp = camera_rtsp.read()
        if not success_rtsp:
            break
        else:
            


            ret_rtsp, buffer_rtsp = cv2.imencode('.jpg', frame_rtsp)
            frame_rtsp = buffer_rtsp.tobytes()
            # Concatenate frame and yield for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_rtsp + b'\r\n') 
            elapsed_time = time.time() - start_time
            logging.debug(f"Frame generation time: {elapsed_time} seconds")

def generate_rgb_frames():
    camera_rgb = cv2.VideoCapture('C:/project/Airfire/src/assets/Videostream/FireDetection.avi')  
    while True:
        start_time = time.time()
        success_rgb, frame_rgb = camera_rgb.read()
        if not success_rgb:
            break
        else:
            ret_rgb, buffer_rgb = cv2.imencode('.jpg', frame_rgb)
            frame_rgb = buffer_rgb.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_rgb + b'\r\n') 
        elapsed_time = time.time() - start_time
        logging.debug(f"AVI Frame generation time: {elapsed_time} seconds")

def generate_thermal_frames():
    camera_thermal = cv2.VideoCapture('C:/project/Airfire/src/assets/Videostream/Thermal.avi')  
    while True:
        start_time = time.time()
        success_thermal, frame_thermal = camera_thermal.read()
        if not success_thermal:
            break
        else:
            ret_thermal, buffer_thermal = cv2.imencode('.jpg', frame_thermal)
            frame_thermal = buffer_thermal.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_thermal + b'\r\n') 
        elapsed_time = time.time() - start_time
        logging.debug(f"AVI Frame generation time: {elapsed_time} seconds")


# Protable Weather Station Readings
def portable_weather_station_read():
    # RS485 USB Configuration
    port = '/dev/ttyUSB0'  # Replace if your USB adapter uses a different port
    baudrate = 9600        # Adjust if your device uses a different baud rate
    parity = 'N'
    stopbits = 1
    bytesize = 8

    # Modbus Slave Configuration
    client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate,
                                parity=parity, stopbits=stopbits, bytesize=bytesize,
                                timeout=2000)   # Adjust timeout if needed

    slave_id = 0x02           # ID of your Modbus slave device
    register_address_list = [0x1F4, 0x1F6, 0x1F8, 0x1F9]    # [WindSpeed, WindDir, Hum, Temp]
    count = 1               # Number of registers to read

    data_list = []

    # Connect to the device
    client.connect()

    # Read data
    for register_address in register_address_list:
        result = client.read_holding_registers(register_address, count, unit=slave_id)
        if not result.isError():
            data_list.append(result.registers[0])
            #print(len(result.registers))
        else:
            data_list.append('error')
            print(f'Error reading registers : {register_address}: {result}')

    # Process the result
    print(f'Wind Speed: {data_list[0]/100} m/s')
    print(f'Wind Direction: {data_list[1]}')
    print(f'Humidity: {data_list[2]/10} %')
    print(f'Temperature: {data_list[3]/10} C')
    # Close the connection
    client.close()

    return data_list


# Route to stream video frames
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/rgb_feed')
def rgb_feed():
    return Response(generate_rgb_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/thermal_feed')
def thermal_feed():
    return Response(generate_thermal_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/weather_station')
def weather_station():
    return Response(portable_weather_station_read(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Run the Flask app+
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')