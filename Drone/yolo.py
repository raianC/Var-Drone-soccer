from ultralytics import YOLO

model = YOLO("runs/detect/train13/weights/best.pt")

results = model.predict(
    source="Drone/test/images",
    conf=0.5,
    save=True
)

print(results)