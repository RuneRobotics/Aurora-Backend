from ultralytics import YOLO
import cv2

class YOLOv8Detector:
    def __init__(self, model_path):

        self.model = YOLO(model_path)

    def detect(self, image):

        results = self.model(image)
        
        bboxes = results[0].boxes.xyxy.cpu().numpy()
        scores = results[0].boxes.conf.cpu().numpy()
        class_ids = results[0].boxes.cls.cpu().numpy()

        return bboxes, scores, class_ids