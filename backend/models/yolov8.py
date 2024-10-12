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

def load_existing_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

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

def open_stream(port: int):

    cap = cv2.VideoCapture(port)

    if not cap.isOpened():
        print("Error: Could not open video stream from webcam.")
        exit()
    
    return cap

def object_detection_process(port, path: str):
    yolo_detector = YOLOv8Detector('yolov8n.pt')
    
    cap = open_stream(port)
    
    data_file = path

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image from webcam.")
            break

        detection_data, output_frame = detect_objects(yolo_detector=yolo_detector, frame=frame)

        cv2.imshow('YOLOv8 Webcam Detection', output_frame)

        # Save data to JSON file after processing the frame
        save_data(data_file, detection_data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    object_detection_process(0, 'data.json')