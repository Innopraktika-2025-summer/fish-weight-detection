from ultralytics import YOLO
'''model = YOLO("yolov8n.pt")'''
'''results = model.predict(source="", conf=0.5,save=True,show=True)'''
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
        annotated_frame = results[0].plot()
        boxes = results[0].boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            width = x2 - x1
            height = y2 - y1
            area = width * height
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            class_id = int(box.cls)
            class_name = model.names[class_id]
            confidence = float(box.conf)
            data = []
            data.append({"class id": class_id,  # frame data
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
            print("class id:", class_id)
            print("class name:", class_name)
            print("x1:", x1)
            print("y1:", y1)
            print("x2:", x2)
            print("y2:", y2)
            print("width:", width)
            print('height:', height)
test=model('20250705_145850.jpg', 0.5, 'C:/ML/Yolo_model/best.pt')
test.load_model()
test.res('photo_2025-07-08_14-52-02.jpg')
'''https://ultralytics.com/images/bus.jpg'''





