import cv2
from collections import deque

duree=10
fps=30
buffer = deque(maxlen=duree*fps)  # Adjust the buffer size as needed
capteurs ={
    "but_equipe1":0,
    "but_equipe2":0,
    "faute":0
}
class VideoRecorder:
    
    def __init__(self):
        self.buffer = deque(maxlen=duree*fps)  # Adjust the buffer size as needed
        self.capteurs = {}
    def ajouter_image(self, frame):
        self.buffer.append(frame)


    def enregistrer_video(self, nom_fichier):
    
        self.capteurs[nom_fichier]+=1
    
        nom_fichier = f"{nom_fichier}_{self.capteurs[nom_fichier]}.avi"
        if len(self.buffer) == 0:
            print("Buffer is empty, no video to save.")
            return
    
        height, width, _ = self.buffer[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video= cv2.VideoWriter(nom_fichier, fourcc, fps, (width, height))
    
        for frame in self.buffer:
            video.write(frame)
    
        video.release()
    
        print(f"Video saved as {nom_fichier}")