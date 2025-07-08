import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO
import pandas as pd
from yolo import model

yolo=model(0.5, 'yolo11x.pt')
yolo.load_model()



def saving_on_desktop():
    # Получаем путь к рабочему столу
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

    # Создаем папку для снимков на рабочем столе (если её нет)
    save_folder = os.path.join(desktop, 'Camera_Shots')
    os.makedirs(save_folder, exist_ok=True)
    return save_folder


def connection_of_cameras():
    # Подключаемся к камере (глаз №0)
    camera = cv2.VideoCapture(0)
    return camera


def photo_size(camera, dlina, visota):
    # размер
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, dlina)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, visota)


def check_cameras(camera):
    # Проверяем, открылась ли камера
    if 0 == camera.isOpened():
        print("Cam is not connected")
        exit()
    print("Connected. Press Q to quit")


def capture_cameras(camera):
    N = 0
    # Захватываем кадр
    frame = []
    frame = camera.read()
    # Если не получилось — выходим
    if 0 == frame[0]:
        print("Frame isn't recieved")
        N = 1
    return frame, N


def photo_output(frame):
    # Показываем кадр
    cv2.imshow("Live Camera", frame[1])


def saving_photo(frame):

        # Создаем имя файла с текущей датой и временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}.jpg"
        return filename, timestamp

def saving_photo_1(frame,filename,save_folder):        # Сохраняем изображение
    if frame[0]:
        filepath = os.path.join(save_folder, filename)
        cv2.imwrite(filepath, frame[1])
        print(f"Frame saved: {filepath}")
    else:
        print("Frame isn't saved")



def closing_the_screen(camera):
    # Убираем за собойq
    camera.release()
    cv2.destroyAllWindows()


def end(camera):
    # Убираем за собойq
    camera.release()
    cv2.destroyAllWindows()


def dict_1(dict1, N, frame, timestamp, result):
    # dict1 = {time.time():{frame,time}}
    dict2 = {N: [frame, timestamp, result]}
    dict1.append(dict2)
    return dict1


def start_vidio(dict1, camera, save_folder):
    N = 1
    result = 1  # kik
    while True:

        frame, N = capture_cameras(camera)

        '''photo_output(frame)'''
        filename, timestamp = saving_photo(frame)
        '''saving_photo_1(frame,filename,save_folder)'''
        result, annotated_frame=yolo.res(frame[1])

        #photo_output(result)
        dict_1(dict1, N, frame, timestamp, result)
        # Выход при нажатии Q
        if cv2.waitKey(1) == ord('q') & 0xFF == ord('q'):
            N = 0
            #closing_the_screen(camera)
            #end(camera)
            return dict1
        N += 1
        cv2.imshow('video', annotated_frame)
        time.sleep(0.5)

class camera:
    def __init__(self):
        pass
    def main(self):
        dict1=[]
        '''save_folder = saving_on_desktop()'''
        save_folder = 1#kik if save_folder = saving_on_desktop() ne comment
        camera = connection_of_cameras()
        photo_size(camera,1920,1080)
        check_cameras(camera)
        start_vidio(dict1, camera, save_folder)
        end(camera)
webcam=camera()
webcam.main()