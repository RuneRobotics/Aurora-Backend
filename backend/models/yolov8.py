from ultralytics import YOLO
import cv2
import logging

# Set logging level to WARNING to suppress INFO and DEBUG logs from YOLOv8
logging.getLogger("ultralytics").setLevel(logging.WARNING)

class YOLOv8Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)  # YOLO model initialization

    def detect(self, image):
        results = self.model(image)  # Perform detection

        bboxes = []
        scores = []
        class_ids = []

        for result in results:
            for box in result.boxes:
                bboxes.append(box.xyxy.cpu().numpy())
                scores.append(box.conf.cpu().numpy())
                class_ids.append(box.cls.cpu().numpy())

        return bboxes, scores, class_ids

    def draw_detections(self, image, bboxes, scores, class_ids):
        for box, score, class_id in zip(bboxes, scores, class_ids):

            box = box.flatten()
            
            score = score.item()
            class_id = class_id.item()

            # Draw the bounding boxes and labels on the image
            cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
            
            label = f"ID: {int(class_id)} | Score: {score:.2f}"
            cv2.putText(image, label, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return image

if __name__ == "__main__":
    yolo_detector = YOLOv8Detector('yolov8n.pt')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream from webcam.")
        exit()

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image from webcam.")
            break

        bboxes, scores, class_ids = yolo_detector.detect(frame)

        output_frame = yolo_detector.draw_detections(frame, bboxes, scores, class_ids)

        cv2.imshow('YOLOv8 Webcam Detection', output_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
