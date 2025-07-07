import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO


desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

#
save_folder = os.path.join(desktop, 'Camera_Shots')
os.makedirs(save_folder, exist_ok=True)


camera = cv2.VideoCapture(0)


if 0 == camera.isOpened():
    print("Камера не подключена")
    exit()
class model:
    def __init__(self, src:str, conf1=float, name=str):
        self.src=src
        self.conf1=conf1
        self.name=name
    def load_model(self):
        global model
        model = YOLO(self.name)
    def res(self,sorc):
        results = model.predict(source=sorc, conf=self.conf1, save=True, show=True)

test=model('20250705_145850.jpg', 0.5, 'yolo11x.pt')
test.load_model()

print("Камера работает. Нажми Q, чтобы выйти")
while True:
    t = time.time()


    a = []
    a = camera.read()

    if 0 == a[0]:
        print("Не могу получить кадр...")
        break
    cv2.imshow("Live Camera", a[1])
    if a[0]:
        # Создаем имя файла с текущей датой и временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(save_folder, filename)

        # Сохраняем изображение
        cv2.imwrite(filepath, a[1])
        print(f"Снимок сохранен: {filepath}")

    else:
        print("Не удалось сделать снимок")
    # Выход при нажатии Q
    if cv2.waitKey(1) == ord('q') & 0xFF == ord('q'):
        break
    time.sleep(0.5)
    test.res(filepath)
camera.release()
cv2.destroyAllWindows()