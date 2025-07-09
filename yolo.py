from ultralytics import YOLO #import of neurolink package
import pandas as pd
import cv2
class model:            #creating model class
    def __init__(self, conf1=float, name=str):
        self.conf1=conf1
        self.name=name
    def load_model(self):
        global model
        model = YOLO(self.name)
    def res(self,frame):
        results = model.predict(source=frame, conf=self.conf1, save=False, show=False)
        annotated_frame = results[0].plot()

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
            data.append({"class id": class_id,          #frame data
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
            return (df), (annotated_frame)