from PySide6.QtWidgets import QLabel, QDialog, QVBoxLayout, QComboBox, QDialogButtonBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from collections import deque
import time
import os
import cv2


def _lister_cameras(max_test=5):
    """Retourne la liste des indices de caméras disponibles."""
    cameras = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append(i)
            cap.release()
    return cameras


class CameraSelectDialog(QDialog):
    """Boîte de dialogue pour choisir la caméra parmi celles disponibles."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choisir la caméra")
        self.setModal(True)
        self.setMinimumWidth(300)

        self.cameras = _lister_cameras()
        self.camera_choisie = self.cameras[0] if self.cameras else 0

        layout = QVBoxLayout()

        label = QLabel("Sélectionnez le flux caméra :")
        self.combo = QComboBox()

        if self.cameras:
            for idx in self.cameras:
                self.combo.addItem(f"Caméra {idx}", idx)
        else:
            self.combo.addItem("Aucune caméra détectée", 0)

        self.combo.currentIndexChanged.connect(self._on_change)

        boutons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boutons.accepted.connect(self.accept)
        boutons.rejected.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(self.combo)
        layout.addWidget(boutons)
        self.setLayout(layout)

    def _on_change(self, index):
        self.camera_choisie = self.combo.itemData(index)

    def get_camera_index(self):
        return self.camera_choisie


class CameraWidget:
    """
    Affiche un flux caméra en direct dans un QLabel positionné en bas à gauche de la fenêtre.
    Une boîte de dialogue s'ouvre au démarrage pour choisir la caméra.

    Utilisation dans main.py :
        from camera import CameraWidget
        cam = CameraWidget(interface, largeur_ecran, hauteur_ecran)
        cam.start()           # ouvre la sélection puis démarre
        cam.changer_camera()  # pour changer de caméra à la volée
        cam.stop()            # pour arrêter
    """

    def __init__(self, parent, largeur_ecran, hauteur_ecran):
        self.parent = parent
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.camera_index = 0
        self.capture = None
        self.fps = 30  
        self.duree_buffer=10
        self.buffer = deque(maxlen=self.duree_buffer * self.fps)
        
        self.compteurs ={
            "but_equipe1":0,
            "but_equipe2":0,
            "faute":0
        }

        # Dimensions : même taille que chrono/score (moitié écran)
        self.cam_width = largeur_ecran // 2
        self.cam_height = hauteur_ecran // 2

        # Position : bas à gauche (sous le chrono)
        x = 0
        y = hauteur_ecran // 2

        self.label = QLabel(parent)
        self.label.setGeometry(x, y, self.cam_width, self.cam_height)
        self.label.setStyleSheet(
            "color: white; font-size: 14px;"
            "border: 2px solid white; background-color: black;"
        )
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Caméra non démarrée")
        self.label.hide()  # caché jusqu'à cam.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)

    def start(self):
        """Ouvre la boîte de sélection de caméra puis démarre le flux."""
        self.label.show()
        self.label.raise_()
        dialog = CameraSelectDialog(self.parent)
        if dialog.exec() == QDialog.Accepted:
            self.camera_index = dialog.get_camera_index()
            self._demarrer_capture()
        else:
            self.label.setText("Caméra\nannulée")

    def changer_camera(self):
        """Ouvre la sélection pour changer de caméra sans relancer l'app."""
        self.stop()
        self.start()

    def stop(self):
        """Arrête la capture caméra et libère les ressources."""
        self.timer.stop()
        if self.capture and self.capture.isOpened():
            self.capture.release()
            self.capture = None
        self.label.clear()
        self.label.setText("Caméra arrêtée")

    def _demarrer_capture(self):
        """Démarre la capture sur l'index choisi."""
        self.capture = cv2.VideoCapture(self.camera_index)
        if not self.capture.isOpened():
            self.label.setText(f"Caméra {self.camera_index}\nindisponible")
            return
        self.label.setText("")
        self.timer.start(33)  # ~30 fps

    def _update_frame(self):
        """Lit une frame et l'affiche dans le label."""
        if self.capture is None or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        self.buffer.append(frame.copy()) 
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qt_image = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(
            self.cam_width,
            self.cam_height,
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation,
        )
        self.label.setPixmap(pixmap)
        
    def enregistrer_video(self, nom_fichier):
        if len(self.buffer) == 0:
            print("Buffer is empty, no video to save.")
            return
        if nom_fichier not in self.compteurs:
            self.compteurs[nom_fichier] = 0
        self.compteurs[nom_fichier] += 1
        dossier = "Videos"
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            
        nom_fichier_complet = os.path.join(dossier, f"{nom_fichier}_{self.compteurs[nom_fichier]}.avi")
        height, width, _ = self.buffer[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(nom_fichier_complet, fourcc, self.fps, (width, height))
        for frame in self.buffer:
            video.write(frame)
        video.release()
        
        print(f"Video saved as {nom_fichier_complet}")
        