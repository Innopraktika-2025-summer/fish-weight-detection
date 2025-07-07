import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO
import pandas as pd


'''esktop = os.path.join(os.path.expanduser('~'), 'Desktop')

#
save_folder = os.path.join(desktop, 'Camera_Shots')
os.makedirs(save_folder, exist_ok=True)'''


camera = cv2.VideoCapture(0)


if 0 == camera.isOpened():
    print("Камера не подключена")
    exit()
class model:
    def __init__(self, conf1=float, name=str):
        self.conf1=conf1
        self.name=name
    def load_model(self):
        global model
        model = YOLO(self.name)
    def res(self,src):
        results = model.predict(source=src, conf=self.conf1, save=False, show=True)
        boxes=results[0].boxes
        for box in boxes:
            x1, y1 ,x2, y2 = box.xyxy[0].tolist()
            width = x2 - x1
            height = y2 - y1
            area = width * height
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            class_id=int(box.cls)
            class_name=model.names[class_id]
            confidence=float(box.conf)
            data=[]
            data.append({"class id": class_id,
                         "class name": class_name,
                         "confidence": confidence,
                         "x1": x1,
                         "y1": y1,
                         "x2": x2,
                         'y2': y2,
                         "width": width,
                         'height': height,
                         "area": area,
                         "center_x": center_x,
                         "center_y": center_y})
            df = pd.DataFrame(data)
            return df

test=model(0.5, 'yolo11x.pt')
test.load_model()

print("Камера работает. Нажми Q, чтобы выйти")
while True:
    t = time.time()


    image = []
    image = camera.read()

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

camera.release()
cv2.destroyAllWindows()