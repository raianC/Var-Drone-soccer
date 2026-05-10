# ATTENTION à chaque fois qu'un but aura été détecté il faudra modifier les varaibles score1 et/ou score2 puis obligatoirement faire points.update_score() pour mettre à jour l'affichage

from timer import Timer
from score import Score

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer, Qt

score1 = 0
score2 = 0
score1_total=0
score2_total=0

duree_penalite_accordee_equipe1 = 10
duree_penalite_accordee_equipe2 = 10
duree_match = 20

nombre_sets = 0
numero_set = 1

app = QApplication(sys.argv)

interface = QWidget()
interface.setWindowTitle("Interface")


def start_set():
    timer_match.start(1000)
    bouton_start.hide()


def choisir_2_sets():
    global nombre_sets

    nombre_sets = 2

    bouton_2sets.hide()
    bouton_3sets.hide()
    texte_accueil.hide()

    bouton_start.show()
    chrono.show()
    score.show()


def choisir_3_sets():
    global nombre_sets

    nombre_sets = 3

    bouton_2sets.hide()
    bouton_3sets.hide()
    texte_accueil.hide()

    bouton_start.show()
    chrono.show()
    score.show()

chrono = QLabel(interface)
chrono.setAlignment(Qt.AlignCenter)
chrono.setText("0:0")
chrono.setStyleSheet(
    "color:white; font-size:40px;border:2px solid white;"
)
chrono.hide()

bouton_quitter = QPushButton("Quitter", interface)


bouton_start = QPushButton(f"START SET {numero_set}", interface)
bouton_start.hide()

bouton_2sets = QPushButton("2 sets", interface)
bouton_3sets = QPushButton("3 sets", interface)

score = QLabel(interface)
score.setAlignment(Qt.AlignCenter)
score.setStyleSheet(
    "color:white; font-size:40px;border:2px solid white;"
)
score.hide()


texte_accueil = QLabel(interface)
texte_accueil.setText("Bonjour !\nCombien de sets voulez-vous réaliser ?")
texte_accueil.setAlignment(Qt.AlignCenter)
texte_accueil.setStyleSheet(
    "color:white; font-size:40px; font-weight:bold;"
)



interface.showFullScreen()




largeur_ecran = interface.width()
hauteur_ecran = interface.height()

bouton_quitter.setGeometry(
    largeur_ecran - largeur_ecran // 20,
    0,
    largeur_ecran // 20,
    hauteur_ecran // 20
)
bouton_quitter.raise_()
bouton_quitter.clicked.connect(interface.close)

# Bouton 2 sets
bouton_2sets.setGeometry(
    largeur_ecran // 2 - largeur_ecran // 10 - 20,
    hauteur_ecran // 2,
    largeur_ecran // 10,
    hauteur_ecran // 10
)
bouton_2sets.clicked.connect(choisir_2_sets)

# Bouton 3 sets
bouton_3sets.setGeometry(
    largeur_ecran // 2 + 20,
    hauteur_ecran // 2,
    largeur_ecran // 10,
    hauteur_ecran // 10
)
bouton_3sets.clicked.connect(choisir_3_sets)

# texte accueil
texte_accueil.setGeometry(
    0,
    hauteur_ecran // 4,
    largeur_ecran,
    hauteur_ecran // 6
)


# Bouton START
bouton_start.setGeometry(
    (largeur_ecran // 2) - largeur_ecran // 10,
    (hauteur_ecran // 2) - hauteur_ecran // 10,
    largeur_ecran // 10,
    hauteur_ecran // 10
)
bouton_quitter.raise_()
bouton_start.clicked.connect(start_set)

score.setGeometry(
    largeur_ecran // 2,
    0,
    largeur_ecran // 2,
    hauteur_ecran // 2
)

chrono.setGeometry(
    0,
    0,
    largeur_ecran // 2,
    hauteur_ecran // 2
)







timer_match = QTimer()

timer = Timer(
    duree_match,
    duree_penalite_accordee_equipe1,
    duree_penalite_accordee_equipe2,
    chrono,
    timer_match
)

points = Score(score1, score2, score)
points.update_score()


timer_match.timeout.connect(timer.update_timer_match)

sys.exit(app.exec())