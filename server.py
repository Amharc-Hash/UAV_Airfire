from flask import Flask, jsonify, Response,request
from flask_cors import CORS  # Import CORS
from pymodbus.client.sync import ModbusSerialClient
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import copy
import logging
import time
import sys , os
sys.path.append(os.path.abspath("/home/portableunit/Project/darknet"))
from darknet import load_network
from darknet_images import image_detection

cfg = '/home/portableunit/Project/darknet/cfg/yolov4-tiny.cfg'
datafile = '/home/portableunit/Project/UAV_Airfire/obj.data'
weights = '/home/portableunit/Project/UAV_Airfire/yolov4-tiny_last.weights'
network, class_names, class_colors = load_network(cfg, datafile,  weights, 1)

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
                # frame_rtsp = model_detect(frame_rtsp)
                ret_rtsp, buffer_rtsp = cv2.imencode('.jpg', frame_rtsp)
                frame_rtsp = buffer_rtsp.tobytes()
                # Concatenate frame and yield for streaming
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_rtsp + b'\r\n') 
                # elapsed_time = time.time() - start_time
                # logging.debug(f"Frame generation time: {elapsed_time} seconds")

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Replace this with your actual data fetching/generation logic
def get_sensor_data():
    data_list = []
    wind_dir = ['S','SW','W','NW','N','NE','E','SE']
    wind_dir_send = 'Z'

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
    #print(f'Wind Speed: {data_list[0]/100} m/s')
    #print(f'Wind Direction: {wind_dir[data_list[1]]}')
    #print(f'Humidity: {data_list[2]/10} %')
    #print(f'Temperature: {data_list[3]/10} C')
    # Close the connection
    client.close()

    if data_list[0] == 0:
        wind_dir_send = 0
    else:
        wind_dir_send = wind_dir[data_list[1]]

    # Create a dictionary for easy use in Vue
    return {
        'valueTemp': data_list[3]/10,
        'windSpeed': data_list[0]/100,
        'windDirec': wind_dir_send,
        'humidity':  data_list[2]/10
    }


@app.route('/weather_data')
def weather():
    response = jsonify(get_sensor_data())
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    return response

def model_detect(input):
    thresh = 0.25
    image, detections = image_detection(
                                    input, 
                                    network, 
                                    class_names, 
                                    class_colors, 
                                    thresh
                                    )
    

    return detections ,image

def rgb_detect(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    l_w = np.array([0,0,200])
    u_w = np.array([180,50,255])
    l_r1 = np.array([0,100,100])
    u_r1 = np.array([10,255,255])
    l_r2 = np.array([170,100,100])
    u_r2 = np.array([180,255,255])
    l_o = np.array([10,100,100])
    u_o = np.array([30,255,25])
    mask_white = cv2.inRange(hsv_image,l_w,u_w)
    mask_red1 = cv2.inRange(hsv_image,l_r1,u_r1)
    mask_red2 = cv2.inRange(hsv_image,l_r2,u_r2)
    mask_orannge = cv2.inRange(hsv_image,l_o,u_o)

    mask = cv2.bitwise_or(mask_white,mask_red1)
    mask = cv2.bitwise_or(mask,mask_red2)
    mask = cv2.bitwise_or(mask,mask_orannge)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours :
        x ,y ,w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50 :
            cv2.rectangle(image, (x,y), (x + w,y + h),(0 , 255, 0), 2)
            fire_found = True
    return fire_found , image

@app.route('/rgb_feed')
def rgb_feed():
    camera_rtsp = cv2.VideoCapture('rtsp://192.168.144.10:8554/H264Video')
    def generate_rgb_frames():
        # while True:
        #     start_time = time.time()
        #     success_rgb, frame_rgb = camera_rgb.read()
        #     if not success_rgb:
        #         break
        #     else:
        #         detections ,frame_rgb = model_detect(frame_rgb)
        #         if len(detections) != 0:
        #             fire_analysis(True)
        #         ret_rgb, buffer_rgb = cv2.imencode('.jpg', frame_rgb)
        #         frame_rgb = buffer_rgb.tobytes()
        #         yield (b'--frame\r\n'
        #             b'Content-Type: image/jpeg\r\n\r\n' + frame_rgb + b'\r\n') 
        #     elapsed_time = time.time() - start_time
        #     logging.debug(f"AVI Frame generation time: {elapsed_time} seconds")
        while True:
            # start_time = time.time()
            success_rtsp, frame_rtsp = camera_rtsp.read()
            if not success_rtsp:
                break
            else:
                # frame_rtsp = model_detect(frame_rtsp)
                # detections ,frame_rgb = model_detect(frame_rtsp)
                # if len(detections) != 0:
                #    fire_analysis(True)
                detections ,frame_rgb = rgb_detect(frame_rtsp)
                if detections :
                    fire_analysis(1)
                ret_rtsp, buffer_rgb = cv2.imencode('.jpg', frame_rgb)
                frame_rgb = buffer_rgb.tobytes()
                # Concatenate frame and yield for streaming
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_rgb + b'\r\n')
                # elapsed_time = time.time() - start_time
                # logging.debug(f"Frame generation time: {elapsed_time} seconds")
    return Response(generate_rgb_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



#Function to create fire analysis
class Cell :
    def __init__(self, forest_type, slope,slope_dir,distance,angle,p_ffmc = 0):


        if forest_type == 0 :
            self.fuel_bed_depth =77.317
        elif forest_type == 1 :
            self.fuel_bed_depth = 108.244
        elif forest_type == 2 :
            self.fuel_bed_depth = 54.12244
        elif forest_type == 3 :
            self.fuel_bed_depth = 38.65889
        else :
            self.fuel_bed_depth = 51.0589
        self.slope = slope
        self.slope_dir = slope_dir
        self.p_ffmc = p_ffmc
        self.stack = 0
        self.distance = distance
        self.angle = angle
        self.is_ignited = False


    
    def wind_blowing(self) :
        if self.wind_dir == self.slope_dir:
            return 0
        elif abs(self.wind_dir - self.slope_dir) == 4:
            return 1
        else :
            return 2

    def update_environment(self, wind_dir, wind_speed, temp, rh) :
        self.wind_speed = wind_speed * 196.850394
        self.wind_dir = wind_dir
        self.temp = temp
        self.rh = rh
        self.ffmc = (0.36 * (self.temp + 20) + 0.1 * self.wind_speed * (9.02 - self.rh)) + self.p_ffmc

        if self.slope <= 10 and self.wind_blowing == 1:
            self.wind_adj = 1 + (math.sin(math.radians(self.slope)) /(2 * 1 * math.sin(math.radians(63.212 - 0.351 * self.slope)) ) )
        elif self.slope >= 18 and self.wind_blowing == 0:
            self.wind_adj = 1 + (math.sin(math.radians(self.slope)) /(2 * 1 * math.sin(math.radians(18.536 - 0.590 * self.slope)) ) )
        elif (self.slope > 10 and self.slope < 18) and self.wind_blowing == 2:
            self.wind_adj = 1 + (math.sin(math.radians(self.slope)) /(2 * 1) )
        else :
            self.wind_adj = 1
        
        self.fmc = 147.2 / (self.ffmc + 7.5)
        
    def state_fire(self, time_ignite, distance_fire,locate,stack) :
        self.time_ignite = time_ignite
        self.distance_fire = distance_fire
        self.locate = locate
        self.stack += stack
    
    def get_wind_speed(self)  :
        if self.angle == self.wind_dir or self.angle == self.wind_dir - 1 or self.angle == self.wind_dir + 1:
            return self.wind_speed
        elif self.angle == (abs(self.wind_dir - 180))%360 :
            return -self.wind_dir
        else :
            if abs(self.wind_dir - self.angle) >= 180 :
                return  - (self.wind_speed * math.cos(math.radians(abs(self.wind_dir - self.angle - 180))))
            else:
                return  - (self.wind_speed * math.cos(math.radians(abs(self.wind_dir - self.angle))))
    
    def get_ros(self, angle):
        ros = 1 / self.fuel_bed_depth * 0.936 * (self.wind_speed/ self.wind_adj) * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
        
        if self.wind_speed != 0 :
            if angle == self.wind_dir :
                return ros
            else :
                ros_otherdirection = 1 / self.fuel_bed_depth * 0.936 * (self.wind_speed * math.cos(math.radians(abs(angle - self.wind_dir)))/ self.wind_adj) * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
                #ros = ros_otherdirection
                if ros_otherdirection <= ros*0.2 :  
                    ros = ros*0.2
                else :
                    ros = ros_otherdirection
                #ros = ros - (0.5 * ros_otherdirection)
        else :
            ros = 1 / self.fuel_bed_depth * 0.936 * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
        return ros
    
    def get_ros_val(self):
        ros = 1 / self.fuel_bed_depth * 0.936 * (self.wind_speed/ self.wind_adj) * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
        base_ros = 1 / self.fuel_bed_depth * 0.936 * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
        return ros , base_ros
    def copy_class(self) :
        return copy.copy(self)

def print_ros(grid,N,time):
    ros,base_ros = grid[N//2,N//2].get_ros_val()
    base_ros *= 0.3048 * time
    ros *= 0.3048 * time
    return ros , base_ros

def calculate_distance(p1,p2) :
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def angle_from_center(center_x, center_y, x, y):
    
    dx = x - center_x
    dy = y - center_y
    angle_rad = np.arctan2(dy, dx)
    angle_deg = np.degrees(angle_rad)
    angle_deg = (180 - angle_deg) % 360
    
    return int(angle_deg)


def initialize_grid(N , forest_type):
    grid = np.empty((N, N), dtype=object)
    for i in range(N):
        for j in range(N):
            # Initialize each cell with random parameters
            grid[i, j] = Cell(1, 0, 0, calculate_distance((i,j),(N//2,N//2)), angle_from_center(N//2,N//2,i,j))
            # Add more initialization for parameters as needed
    return grid

def get_data_weatherstation(grid,scale, wind_dir, wind_speed, temp, rh) :
    N = 101
    for i in range(N):
        for j in range(N):
            grid[i,j].update_environment(wind_dir, wind_speed, temp, rh)
            grid[i,j].distance *= scale
    return grid
    

def update(grid, N ,time, scale,fire_found = False):
    if fire_found :
        newGrid = copy.deepcopy(grid)
        for i in range(0,N):
            for j in range(0,N):
                if grid[i,j].is_ignited :
                    for x in range(0,N):
                        for y in range(0,N):
                            if calculate_distance((i,j),(x,y))*scale <= (grid[i,j].get_ros(angle_from_center(i,j,x,y))) * time :
                                newGrid[x,y].stack += 1
                                newGrid[x,y].is_ignited = True
                    #newGrid[i,j].is_ignited = False
        # Update the data of the image object
        return newGrid
    else :
        return grid
    
def color_map(N,grid1,grid2,grid3,grid4) :
    data = np.zeros((N,N))
    value_color_map = {
        0: 'forestgreen',
        1: 'limegreen',
        2: 'yellow',
        3: 'orange',
        4: 'red'
    }
    data += [[cell.stack for cell in row] for row in grid1]
    data += [[cell.stack for cell in row] for row in grid2]
    data += [[cell.stack for cell in row] for row in grid3]
    data += [[cell.stack for cell in row] for row in grid4]
    colors = [value_color_map.get(value, 'white') for value in np.unique(data)]
    cmap = ListedColormap(colors)
    plt.imshow(data, cmap=cmap, interpolation='nearest')
    plt.savefig('src/assets/result/plot.jpg')

def fire_analysis(forest_type) :
    N = 101
    scale = 10
    data = get_sensor_data()
    print(data)
    if data['windDirec'] == 'N' :
        direc = 0
    elif data['windDirec'] == 'NE' :
        direc = 45
    elif data['windDirec'] == 'E' :
        direc = 90
    elif data['windDirec'] == 'SE' :
        direc = 135
    elif data['windDirec'] == 'S' :
        direc = 180
    elif data['windDirec'] == 'SW' :
        direc = 225
    elif data['windDirec'] == 'W' :
        direc = 270
    elif data['windDirec'] == 'NW' :
        direc = 315
    else :
        direc = 0
        data['windSpeed'] = 0
    time = 20
    grid = initialize_grid(N, forest_type)
    grid = get_data_weatherstation(grid,scale, direc, data['windSpeed'], data['valueTemp'], data['humidity'])
    grid[N//2,N//2].is_ignited = True
    grid1 = update(grid,N,time*0.5,scale,True)
    grid2 = update(grid,N,time,scale,True)
    grid3 = update(grid,N,time*1.5,scale,True)
    grid4 = update(grid,N,time*2,scale,True)
    color_map(N,grid1,grid2,grid3,grid4)
    return print_ros(grid,N,time)

@app.route('/fire_bounding')
def fire_bounding():
    ros , base_ros = fire_analysis()
    return {
        'radius1': base_ros,
        'radius2': ros/2
    }

@app.route('/fire_analysis_feed')
def fire_analysis_feed():
    def prediction_show() :
        img = cv2.imread('src/assets/result/plot.jpg')
        ret_rgb, buffer_rgb = cv2.imencode('.jpg', img)
        frame_rgb = buffer_rgb.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_rgb + b'\r\n')
    return Response(prediction_show(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update-time',methods=['POST'])
def update_time():
    data = request.get_json()
    selected_time = data.get('selectedTime')
    print('Select time :',selected_time)
    return 'Time update successfully'

if __name__ == '__main__':

    app.run(debug=True, port=5000)
