from PySide6.QtWidgets import QLabel, QPushButton, QDialog, QVBoxLayout, QComboBox, QDialogButtonBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
import cv2
import os


EXTENSIONS_VIDEO = (".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm")


def _lister_videos(dossier="Videos"):
    """Retourne la liste des fichiers vidéo trouvés dans le dossier."""
    if not os.path.isdir(dossier):
        return []
    return [
        f for f in sorted(os.listdir(dossier))
        if f.lower().endswith(EXTENSIONS_VIDEO)
    ]


class VideoSelectDialog(QDialog):
    """Boîte de dialogue pour choisir une vidéo dans le dossier 'Video'."""

    def __init__(self, parent=None, dossier="Videos"):
        super().__init__(parent)
        self.setWindowTitle("Choisir une vidéo")
        self.setModal(True)
        self.setMinimumWidth(350)
        self.dossier = dossier
        self.video_choisie = None

        layout = QVBoxLayout()

        self.combo = QComboBox()
        videos = _lister_videos(dossier)

        if videos:
            for v in videos:
                self.combo.addItem(v, os.path.join(dossier, v))
            self.video_choisie = os.path.join(dossier, videos[0])
        else:
            self.combo.addItem(f"Aucune vidéo dans '{dossier}'", None)

        self.combo.currentIndexChanged.connect(self._on_change)

        boutons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boutons.accepted.connect(self.accept)
        boutons.rejected.connect(self.reject)

        layout.addWidget(QLabel(f"Vidéos disponibles ({dossier}/) :"))
        layout.addWidget(self.combo)
        layout.addWidget(boutons)
        self.setLayout(layout)

    def _on_change(self, index):
        self.video_choisie = self.combo.itemData(index)

    def get_video_path(self):
        return self.video_choisie


class VideoPlayer(QDialog):
    """Fenêtre de lecture vidéo. Ferme automatiquement en fin de vidéo."""

    def __init__(self, parent, video_path):
        super().__init__(parent)
        self.setWindowTitle("Lecture vidéo")
        self.setModal(True)
        self.resize(800, 500)
        self.timer = QTimer()

        self.capture = cv2.VideoCapture(video_path)
        if not self.capture.isOpened():
            label = QLabel("Impossible d'ouvrir la vidéo :\n" + video_path, self)
            label.setAlignment(Qt.AlignCenter)
            layout = QVBoxLayout()
            layout.addWidget(label)
            self.setLayout(layout)
            return

        fps = self.capture.get(cv2.CAP_PROP_FPS) or 25
        self.interval_ms = int(1000 / fps)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.video_label)
        self.setLayout(layout)

        self.timer.timeout.connect(self._update_frame)
        self.timer.start(self.interval_ms)

    def _update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            self.timer.stop()
            self.capture.release()
            self.accept()
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qt_image = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(
            self.video_label.width(),
            self.video_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.timer.stop()
        if self.capture and self.capture.isOpened():
            self.capture.release()
        super().closeEvent(event)


class VideoButton:
    """
    Bouton qui ouvre d'abord une liste des vidéos du dossier 'Vidéo/',
    puis lit la vidéo choisie dans une fenêtre modale.

    Utilisation dans main.py :
        from video_button import VideoButton
        btn_video = VideoButton(interface, largeur_ecran, hauteur_ecran)
        btn_video.show()

    Le dossier par défaut est 'Vidéo/' (relatif à l'emplacement du script).
    Tu peux le changer : VideoButton(..., dossier="mon_dossier")
    """

    def __init__(self, parent, largeur_ecran, hauteur_ecran, dossier="Vidéo", label="▶ Replay"):
        self.parent = parent
        self.dossier = dossier

        btn_w = largeur_ecran // 8
        btn_h = hauteur_ecran // 14

        # Positionné en bas à droite
        x = largeur_ecran - btn_w - int(0.05 * largeur_ecran)
        y = hauteur_ecran - btn_h - 20

        self.bouton = QPushButton(label, parent)
        self.bouton.setGeometry(x, y, btn_w, btn_h)
        self.bouton.setStyleSheet(
            "color: white; font-size: 18px;"
            "background-color: #222; border: 2px solid white;"
            "border-radius: 6px;"
        )
        self.bouton.clicked.connect(self._choisir_et_lire)
        self.bouton.raise_()

    def show(self):
        self.bouton.show()

    def hide(self):
        self.bouton.hide()

    def _choisir_et_lire(self):
        """Ouvre la sélection de vidéo puis lance la lecture."""
        select = VideoSelectDialog(self.parent, self.dossier)
        if select.exec() == QDialog.Accepted:
            path = select.get_video_path()
            if path:
                player = VideoPlayer(self.parent, path)
                player.exec()