
from ultralytics import YOLO
import torch

from pathlib import Path



def main():
    test_dir = Path(r"C:\yolo_test\weights")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path = test_dir / "test.pt"
    
    torch.save({"test": 1}, test_path)
    print("Sauvegarde PyTorch réussie :", test_path)
        
    print("CUDA disponible :", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU :", torch.cuda.get_device_name(0))
        device = 0
    else:
        print("GPU indisponible")
        device = "cpu"

    model = YOLO("runs/detect/train13/weights/best.pt")

   
    
    
    # Chemin absolu vers le dossier du projet
    project_dir = Path(__file__).resolve().parent.parent
    
    results = model.train(
    data=str(project_dir / "Drone" / "data.yaml"),
    epochs=30,
    imgsz=640,
    batch=8,
    device=0,
    workers=4,
    project="C:\\Users\\raian\\Documents\\GitHub\\Var-Drone-soccer\\results",
    name="train_gpu",
    exist_ok=True
    )
    print(results)


if __name__ == "__main__":
    main()
