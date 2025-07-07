import cv2
import os
import time
from datetime import datetime

# Получаем путь к рабочему столу
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

# Создаем папку для снимков на рабочем столе (если её нет)
save_folder = os.path.join(desktop, 'Camera_Shots')
os.makedirs(save_folder, exist_ok=True)



# Подключаемся к камере (глаз №0)
camera = cv2.VideoCapture(0)

# Проверяем, открылась ли камера
if 0 == camera.isOpened():
    print("Ой! Камера не включена 😢")
    exit()

print("Камера работает! Нажми 'Q', чтобы выйти")
while True:
    t=time.time()

# Захватываем кадр

    a=[]
    a=camera.read()
    # Если не получилось — выходим
    if 0 == a[0]:
        print("Не могу получить кадр...")
        break
    
    # Показываем кадр
    cv2.imshow("Live Camera", a[1])
    if a[0]:
    # Создаем имя файла с текущей датой и временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(save_folder, filename)
    
        # Сохраняем изображение
        cv2.imwrite(filepath, a[1])
        print(f"✅ Снимок сохранен: {filepath}")
    else:
        print("❌ Не удалось сделать снимок")
    # Выход при нажатии Q
    if cv2.waitKey(1) ==ord('q')& 0xFF == ord('q'):
        break
    time.sleep(0.5)    
# Убираем за собойq
camera.release()
cv2.destroyAllWindows()
