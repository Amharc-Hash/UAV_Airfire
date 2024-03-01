# Import necessary modules
from flask import Flask, Response,render_template
import cv2
import logging
import time
import numpy as np
import torch
import torchvision
from torchvision import transforms
from PIL import Image
import math 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import copy

#model setup
model = torch.hub.load('yolov3', 'custom', path='src/components/best.pt', source='local') 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
model.eval()
fire_found = False
N = 101
print('success')
# Create a Flask app instance

app = Flask(__name__, static_url_path='/static')


# Function to generate video frames from the camera
def model_detect(frame_rtsp) :
            classNames = ["fire","smoke"]
            results = model(frame_rtsp)
            obj = results.xyxy[0].cpu().detach().numpy()
            if len(obj) == 0 :
                fire_found = False
            else :
                fire_found = True
            fire_analysis(fire_found)
            for box in obj:
                    # bounding box
                    x1 , y1 ,x2 ,y2 , conf , cls = box
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                    # put box in cam
                    cv2.rectangle(frame_rtsp, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # confidence
                    confidence = math.ceil((conf*100))/100
                    print("Confidence --->",confidence)

                    # class name
                    cls = int(cls)
                    print("Class name -->", classNames[cls])

                    # object details
                    if classNames[cls] == 'fire':
                        color = (0, 0, 255)
                    else :
                        color = (255, 0, 0)
                    cv2.rectangle(frame_rtsp, (x1, y1), (x2, y2), color, 3)
                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    thickness = 2
                    cv2.putText(frame_rtsp, classNames[cls], org, font, fontScale, color, thickness)
            return fire_found, frame_rtsp

def detect_thermal_point(frame):

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_frame, 220, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bounding_boxes.append((x, y, x + w, y + h))
    bounding_boxes = filter_inside_boxes(bounding_boxes)
    return bounding_boxes

def detect_thermal(frame):
    bounding_boxes = detect_thermal_point(frame)
    for box in bounding_boxes:
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
    return frame

def filter_inside_boxes(boxes):
    filtered_boxes = []
    for i, box1 in enumerate(boxes):
        inside = False
        for j, box2 in enumerate(boxes):
            if i != j:
                if box1[0] >= box2[0] and box1[1] >= box2[1] and box1[2] <= box2[2] and box1[3] <= box2[3]:
                    inside = True
                    break
        if not inside:
            filtered_boxes.append(box1)

    return filtered_boxes

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
    camera_rgb = cv2.VideoCapture('rtsp://192.168.144.10:8554/H264Video')  
    while True:
        start_time = time.time()
        success_rgb, frame_rgb = camera_rgb.read()
        if not success_rgb:
            break
        else:
            fire_flag,frame_rgb = model_detect(frame_rgb)
            ret_rgb, buffer_rgb = cv2.imencode('.jpg', frame_rgb)
            frame_rgb = buffer_rgb.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_rgb + b'\r\n') 
        elapsed_time = time.time() - start_time
        logging.debug(f"AVI Frame generation time: {elapsed_time} seconds")

def generate_thermal_frames():
    camera_thermal = cv2.VideoCapture('src/assets/Videostream/Thermal.avi')  
    while True:
        start_time = time.time()
        success_thermal, frame_thermal = camera_thermal.read()
        if not success_thermal:
            break
        else:
            frame_thermal = detect_thermal(frame_thermal)
            ret_thermal, buffer_thermal = cv2.imencode('.jpg', frame_thermal)
            frame_thermal = buffer_thermal.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_thermal + b'\r\n') 
        elapsed_time = time.time() - start_time
        logging.debug(f"AVI Frame generation time: {elapsed_time} seconds")

#Function to create fire analysis
class Cell :
    def __init__(self, fuel_bed_depth, slope,slope_dir,distance,angle,p_ffmc = 0):
        self.fuel_bed_depth = fuel_bed_depth
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
        self.wind_speed = wind_speed * 88
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
        ros = 1 / self.fuel_bed_depth * 0.936 * (self.wind_speed * 54.680665 / self.wind_adj) * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
        
        if self.wind_speed != 0 :
            if angle == self.wind_dir :
                return ros
            else :
                ros_otherdirection = 1 / self.fuel_bed_depth * 0.936 * (self.wind_speed * math.cos(math.radians(abs(angle - self.wind_dir))) * 54.680665 / self.wind_adj) * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
                #ros = ros_otherdirection
                if ros_otherdirection <= ros*0.2 :  
                    ros = ros*0.2
                else :
                    ros = ros_otherdirection
                #ros = ros - (0.5 * ros_otherdirection)
        else :
            ros = 1 / self.fuel_bed_depth * 0.936 * (1 + 3.33 * (self.ffmc/100) * (self.fmc/100))
        return ros
    
    def copy_class(self) :
        return copy.copy(self)

def calculate_distance(p1,p2) :
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def angle_from_center(center_x, center_y, x, y):
    
    dx = x - center_x
    dy = y - center_y
    angle_rad = np.arctan2(dy, dx)
    angle_deg = np.degrees(angle_rad)
    angle_deg = (180 - angle_deg) % 360
    
    return int(angle_deg)


def initialize_grid(N):
    grid = np.empty((N, N), dtype=object)
    for i in range(N):
        for j in range(N):
            # Initialize each cell with random parameters
            grid[i, j] = Cell(1, 0, 0, calculate_distance((i,j),(N//2,N//2)), angle_from_center(N//2,N//2,i,j))
            # Add more initialization for parameters as needed
    return grid

def get_data_weatherstation(grid,scale, wind_dir, wind_speed, temp, rh) :
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
                            if calculate_distance((i,j),(x,y))*scale <= (grid[i,j].get_ros(angle_from_center(i,j,x,y)))*0.00508* time :
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

def fire_analysis(fire_found) :
    if fire_found :
        time = 60
        scale = 10
        wind_dir = 0
        wind_speed = 1
        temp = 32
        rh = 55
        grid = initialize_grid(N)
        grid = get_data_weatherstation(grid,scale, wind_dir, wind_speed, temp, rh)
        grid[N//2,N//2].is_ignited = True
        grid1 = update(grid,N,time*0.5,scale,True)
        grid2 = update(grid,N,time,scale,True)
        grid3 = update(grid,N,time*1.5,scale,True)
        grid4 = update(grid,N,time*2,scale,True)
        color_map(N,grid1,grid2,grid3,grid4)
        
def prediction_show() :
    img = cv2.imread('src/assets/result/plot.jpg')
    ret_rgb, buffer_rgb = cv2.imencode('.jpg', img)
    frame_rgb = buffer_rgb.tobytes()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame_rgb + b'\r\n')

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

@app.route('/fire_analysis_feed')
def fire_analysis_feed():
    return Response(prediction_show(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the Flask app+
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')