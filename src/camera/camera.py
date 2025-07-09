import cv2
import os
from datetime import datetime
from src.model.yolo import YOLOModel


class Camera:
    def __init__(self, width, height, cam_name, confidence_threshold, model_path):
        # Camera parameters
        self.width = width
        self.height = height
        self.cam_name = cam_name
        self.camera = None
        self.save_folder = None
        self.frames_data = []

        # YOLO model parameters
        self.confidence_threshold = confidence_threshold
        self.model_path = model_path
        self.yolo = YOLOModel(self.confidence_threshold, self.model_path)
        
    def initialize(self):
        self.save_folder = self._create_save_directory()
        self.camera = self._connect_camera()
        self._set_resolution()
        self._verify_camera_connection()
        return self.frames_data
        
    def _create_save_directory(self):
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        save_folder = os.path.join(desktop, "Camera_Snapshots")
        os.makedirs(save_folder, exist_ok=True)
        return save_folder

    def _connect_camera(self):
        return cv2.VideoCapture(self.cam_name)

    def _set_resolution(self):
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
    def _verify_camera_connection(self):
        if not self.camera.isOpened():
            print("Camera isn't connected")
            exit()
        print("Camera works! Press Q to quit")

    def capture_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Can't receive frame")
            return None, True
        return frame, False

    def display_frame(self, frame):
        cv2.imshow("Live Camera", frame)

    def save_frame(self, frame):   
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(self.save_folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"Frame saved: {filepath}")
        return timestamp

    def close_windows(self):           
        if self.camera is not None:
            self.camera.release()
        cv2.destroyAllWindows()
    
    def add_frame_data(self, frame_number, frame, timestamp, detection_result):
        frame_data = {frame_number: [timestamp, frame, detection_result]}
        self.frames_data.append(frame_data)
        
    def start_video_capture(self, show_video=True):
        frame_number = 1
        self.frames_data = []
        
        while True:
            frame, error = self.capture_frame()
            if error:
                break
                
            detection_result, annotated_frame = self.yolo.process_frame(frame)
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.add_frame_data(frame_number, frame, timestamp, detection_result)
            
            if show_video:
                cv2.imshow('video', annotated_frame)

            frame_number += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.close_windows()
        
    def run(self):
        self.initialize()
        self.start_video_capture()
        return self.frames_data