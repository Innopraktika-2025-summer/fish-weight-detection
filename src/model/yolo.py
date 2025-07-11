from ultralytics import YOLO
import pandas as pd
import cv2


class YOLOModel:
    def __init__(self, confidence_threshold, model_path):
        self.confidence_threshold = confidence_threshold
        self.model_path = model_path
        self._model = None
        self._load_model()
        
    def _load_model(self):
        self._model = YOLO(self.model_path)
    
    def _process_box(self, box):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        width = x2 - x1
        height = y2 - y1
        
        return {
            "class_id": int(box.cls),
            "class_name": self._model.names[int(box.cls)],
            "confidence": float(box.conf),
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "width": width,
            "height": height,
            "area": width * height,
            "center_x": (x1 + x2) / 2,
            "center_y": (y1 + y2) / 2
        }
    
    def process_frame(self, frame):
        results = self._model.track(
            source=frame, 
            conf=self.confidence_threshold, 
            save=False, 
            show=False
        )
        
        annotated_frame = results[0].plot()
        boxes = results[0].boxes
        
        data = [self._process_box(box) for box in boxes]
        
        df = pd.DataFrame(data)
        return df, annotated_frame