from ultralytics import YOLO
import cv2
import logging
import json
import os

logging.getLogger("ultralytics").setLevel(logging.WARNING)

class YOLOv8Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, image):
        results = self.model(image)

        bboxes = []
        scores = []
        class_ids = []

        for result in results:
            for box in result.boxes:
                bboxes.append(box.xyxy.cpu().numpy().tolist())  # Convert to list for JSON serialization
                scores.append(box.conf.cpu().numpy().tolist()[0])  # Get the first element (confidence score)
                class_ids.append(box.cls.cpu().numpy().tolist()[0])  # Get the first element (class ID)

        return bboxes, scores, class_ids

    def draw_detections(self, image, bboxes, scores, class_ids):
        for box, score, class_id in zip(bboxes, scores, class_ids):
            box = box[0]  # Access the first bounding box
            
            # Extract coordinates
            x1, y1, x2, y2 = map(int, box)  # Convert to integers
            
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # No need to call item() since score and class_id are already single values now
            label = f"ID: {int(class_id)} | Score: {score:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return image

def detect_objects(yolo_detector, frame):
    
    bboxes, scores, class_ids = yolo_detector.detect(frame)

    # Store detection information
    detection_data = {
        "bboxes": bboxes,
        "scores": scores,
        "class_ids": class_ids
    }

    output_frame = yolo_detector.draw_detections(frame, bboxes, scores, class_ids)

    return detection_data, output_frame

def object_detection_process(port, path: str):
    pass