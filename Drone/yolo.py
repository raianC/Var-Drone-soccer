from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(
    data="C:/Users/raian/Documents/GitHub/Var-Drone-soccer/Drone/data.yaml",
    epochs=10,
    imgsz=640,
    batch=4,
    mode="train"
)