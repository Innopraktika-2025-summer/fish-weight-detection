import cv2
import os
import time
from datetime import datetime


def soxranenie_photo_na_rabochiy_stol():
        # Получаем путь к рабочему столу
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Создаем папку для снимков на рабочем столе (если её нет)
    save_folder = os.path.join(desktop, 'Camera_Shots')
    os.makedirs(save_folder, exist_ok=True)
    return save_folder

def podkluchenie_k_camera():
       # Подключаемся к камере (глаз №0)
    camera = cv2.VideoCapture(0)
    return camera

def razmer_photo(camera, dlina, visota):
        #размер
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,dlina)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,visota)
    
def proverka_kamer(camera):
        # Проверяем, открылась ли камера
    if 0 == camera.isOpened():
        print("Ой! Камера не включена 😢")
        exit()
    print("Камера работает! Нажми 'Q', чтобы выйти")

def zaxvat_photo(camera):
            N = 0
                # Захватываем кадр
            izobragenie=[]
            izobragenie=camera.read()
                # Если не получилось — выходим
            if 0 == izobragenie[0]:
                print("Не могу получить кадр...")
                N = 1
            return izobragenie, N
def vivod_photo(izobragenie):
                # Показываем кадр
            cv2.imshow("Live Camera", izobragenie[1])

def soxranenie_photo(izobragenie,save_folder):   
            if izobragenie[0]:
                    # Создаем имя файла с текущей датой и временем
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"photo_{timestamp}.jpg"
                filepath = os.path.join(save_folder, filename)
                    # Сохраняем изображение
                cv2.imwrite(filepath, izobragenie[1])
                print(f"✅ Снимок сохранен: {filepath}")
            else:
                print("❌ Не удалось сделать снимок")
            
def kik_ekran(camera):           
                   # Убираем за собойq
                camera.release()
                cv2.destroyAllWindows()
                
def konetc(camera):
        # Убираем за собойq
    camera.release()
    cv2.destroyAllWindows()


def main():
    save_folder = soxranenie_photo_na_rabochiy_stol()
    camera = podkluchenie_k_camera()
    razmer_photo(camera,1920,1080)
    proverka_kamer(camera)

    N = 0
    while N == 0:

        izobragenie, N = zaxvat_photo(camera)
        vivod_photo(izobragenie)
        soxranenie_photo(izobragenie,save_folder)
            # Выход при нажатии Q
        if cv2.waitKey(1) ==ord('q')& 0xFF == ord('q'):  
            N=1
            kik_ekran(camera)
            konetc(camera)
            return 0
        time.sleep(3)
        

    konetc(camera)


main()
