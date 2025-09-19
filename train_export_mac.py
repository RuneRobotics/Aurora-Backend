from ultralytics import YOLO
import torch

# Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Training on device: {device}")

# Load YOLOv8n model
model = YOLO("yolov8n.pt")

# Train on dataset
results = model.train(
    data="yolo.v5i.yolov8/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    device=device,
    plots=True
)

# Path to best trained weights
best_model_path = "runs/detect/train/weights/best.pt"

# Export to ONNX
print("Exporting to ONNX...")
onnx_model = YOLO(best_model_path)
onnx_model.export(format="onnx", imgsz=640, dynamic=True)

# Export to TensorRT engine (FP16)
print("Exporting to TensorRT engine...")
trt_model = YOLO(best_model_path)
trt_model.export(format="engine", half=True)

print("Training and export complete")
print("ONNX file: best.onnx")
print("TensorRT engine: best.engine")
print("Trained weights: runs/detect/train/weights/best.pt")
