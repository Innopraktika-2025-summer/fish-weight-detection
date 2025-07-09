import cv2
import os
import time
from datetime import datetime
from yolo import model
yolo = model(0.5, 'yolo11x.pt')
yolo.load_model()
class Camera1:
    def __init__(self):
        pass

    def main(self):
        self.dict1 = []
        self.save_folder = self.saving_on_desktop()
        self.camera = self.connection_of_cameras()
        self.photo_size(1920, 1080)
        self.check_cameras()
        self.start_vidio()
        self.end()
        return self.dict1 
        
    def saving_on_desktop(self):
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        save_folder = os.path.join(desktop, "Camera_Snapshots")
        os.makedirs(save_folder, exist_ok=True)
        return save_folder

    def connection_of_cameras(self):
        camera = cv2.VideoCapture(0)
        return camera

    def photo_size(self, dlina, visota):
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, dlina)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, visota)
        
    def check_cameras(self):
        if not self.camera.isOpened():
            print("Ой! Камера не включена 😢")
            exit()
        print("Камера работает! Нажми 'Q', чтобы выйти")

    def capture_cameras(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Не могу получить кадр...")
            return None, 1
        return frame, 0

    def photo_output(self, frame):
        cv2.imshow("Live Camera", frame)

    def saving_photo(self, frame):   
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(self.save_folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"Снимок сохранен: {filepath}")
        return timestamp

    def closing_the_screen(self):           
        self.camera.release()
        cv2.destroyAllWindows()
                    
    def end(self):
        self.camera.release()
        cv2.destroyAllWindows()
        

    def dict_1(self, N, frame, timestamp, result):
        dict2 = {N: [timestamp, frame, result]}
        self.dict1.append(dict2)
        
    def start_vidio(self):
        N = 1
        result = 1
        while True:
            frame, error = self.capture_cameras()
            if error:
                break
            result, annotated_frame = yolo.res(frame)
                
            '''self.photo_output(frame)'''
            '''timestamp = self.saving_photo(frame)'''
            self.dict_1(N, frame, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), result)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.closing_the_screen()
                break
            cv2.imshow('video', annotated_frame)
            N += 1
            '''time.sleep(3)'''
            
webcam=Camera1()
webcam.main()
