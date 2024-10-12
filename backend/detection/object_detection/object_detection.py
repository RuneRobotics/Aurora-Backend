from ultralytics import YOLO
import cv2
class ObjectDetector:
    def __init__(self, model_path, valid_ids, conf_limit=0):
        self.model = YOLO(model_path)
        self.conf_limit = conf_limit
        self.valid_ids = valid_ids

    def detect(self, image):
        results = self.model(image)

        bboxes = []
        scores = []
        class_ids = []

        for result in results:
            for box in result.boxes:
                if box.conf.cpu().numpy() > self.conf_limit and box.cls.cpu().numpy() in self.valid_ids: 
                    bboxes.append(box.xyxy.cpu().numpy().tolist())  # Convert to list for JSON serialization
                    scores.append(box.conf.cpu().numpy().tolist()[0])  # Get the first element (confidence score)
                    class_ids.append(box.cls.cpu().numpy().tolist()[0])  # Get the first element (class ID)

        return bboxes, scores, class_ids

    def draw_detections(self, image, bboxes, scores, class_ids):
        for box, score, class_id in zip(bboxes, scores, class_ids):
            
            box = box[0]
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            label = f"ID: {int(class_id)} | Score: {score:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return image

def detect_objects(object_detector, frame):
    
    bboxes, scores, class_ids = object_detector.detect(frame)

    notes_data = {"notes": [{"x": (xyxy[0][0] + xyxy[0][2]) / 2, "y": (xyxy[0][1] + xyxy[0][3]) / 2, "score": score} for xyxy, score in zip(bboxes, scores)]}

    output_frame = object_detector.draw_detections(frame, bboxes, scores, class_ids)

    detection_data = notes_data # | robot_data | etc...

    return detection_data, output_frame