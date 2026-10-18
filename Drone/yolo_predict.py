
from ultralytics import YOLO
import torch
from pathlib import Path

def main():
    model = YOLO(
        r"C:\Users\raian\Documents\GitHub\Var-Drone-soccer\training\train_gpu\weights\best.pt"
    )

    video_path = Path("Drone") / "Video Project 6.mp4"

    results = model.predict(
        source=str(video_path),
        conf=0.3,
        save=True,
        show=False,
        device=0 if torch.cuda.is_available() else "cpu"
    )
    print(results)


if __name__ == "__main__":
    main()
