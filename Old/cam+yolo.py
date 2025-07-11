import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO
import pandas as pd
from src.model.yolo import model


'''esktop = os.path.join(os.path.expanduser('~'), 'Desktop')

#
save_folder = os.path.join(desktop, 'Camera_Shots')
os.makedirs(save_folder, exist_ok=True)'''




cam = cv2.VideoCapture(0)


if 0 == cam.isOpened():
    print("Камера не подключена")
    exit()


test=model(0.5, 'yolo11x.pt')
test.load_model()
def photo_scale(cam, width, height):
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
print("Камера работает. Нажми Q, чтобы выйти")
while True:
    photo_scale(cam, 1920, 1080)
    t = time.time()


    image = []
    image = cam.read()

    if 0 == image[0]:
        print("Не могу получить кадр...")
        break
    cv2.imshow("Live Camera", image[1])
    if image[0]:
        '''# Создаем имя файла с текущей датой и временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(save_folder, filename)

        # Сохраняем изображение
        cv2.imwrite(filepath, a[1])
        print(f"Снимок сохранен: {filepath}")'''
        test.res(image[1])

    else:
        print("Не удалось сделать снимок")
    # Выход при нажатии Q
    if cv2.waitKey(1) == ord('q') & 0xFF == ord('q'):
        break
    time.sleep(0.5)

cam.release()
cv2.destroyAllWindows()