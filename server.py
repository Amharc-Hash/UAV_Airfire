from flask import Flask, jsonify, Response
from flask_cors import CORS  # Import CORS
from pymodbus.client.sync import ModbusSerialClient
import cv2
import logging
import time

app = Flask(__name__)
CORS(app)


# Video Streaming route
@app.route('/video_feed')
def video_feed():
    # Replace with the actual RTSP address
    camera_rtsp = cv2.VideoCapture('rtsp://192.168.144.10:8554/H264Video')
    def generate_frames():
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

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Replace this with your actual data fetching/generation logic
def get_sensor_data():
    data_list = []
    wind_dir = ['S','SW','W','NW','N','NE','E','SE']

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
    print(f'Wind Direction: {wind_dir[data_list[1]]}')
    print(f'Humidity: {data_list[2]/10} %')
    print(f'Temperature: {data_list[3]/10} C')
    # Close the connection
    client.close()

    # Create a dictionary for easy use in Vue
    return {
        'valueTemp': data_list[3]/10,
        'windSpeed': data_list[0]/100,
        'windDirec': wind_dir[data_list[1]],
        'humidity':  data_list[2]/10
    }

@app.route('/weather_data')
def weather():
    response = jsonify(get_sensor_data())
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)