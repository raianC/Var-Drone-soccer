# ATTENTION à chaque fois qu'un but aura été détecté il faudra modifier les varaibles score1 et/ou score2 puis obligatoirement faire points.update_score() pour mettre à jour l'affichage



from timer import Timer
from score import Score

import sys
from PySide6.QtWidgets import * #importe tous les widgets 
from PySide6.QtCore import QTimer, Qt #nécessaire Qtimer


score1=0
score2=0
duree_penalite=10
duree_match=20

app = QApplication(sys.argv)
interface=QWidget()                    #création fenêtre vide
interface.setWindowTitle("Interface")     # Titre de la fenêtre
#interface.resize(400, 400)             # Taille de la fenêtre (largeur x hauteur)


def start_match():
    timer_match.start(1000)
    bouton_start.hide()


chrono = QLabel(interface)
chrono.setAlignment(Qt.AlignCenter) # aligne l'écriture au centre du label
chrono.setText("0:0")
chrono.setStyleSheet("color:white; font-size:40px;border:2px solid white;")

bouton_quitter = QPushButton("Quitter", interface)
bouton_start = QPushButton("START CHRONO", interface)

score=QLabel(interface)
score.setAlignment(Qt.AlignCenter) # aligne l'écriture au centre du label
score.setStyleSheet("color:white; font-size: 40px;border:2px solid white;")  # augmente la taille d'écriture du chrono                      

interface.showFullScreen() #montre la fenêtre (Attention, montrer après avoir créé les labels)

largeur_ecran = interface.width()
hauteur_ecran = interface.height()


#bouton_quitter.setGeometry(largeur_ecran-60,10, 55, 55)  # setGeometry(x, y, width, height)
bouton_quitter.setGeometry(largeur_ecran-0.05*largeur_ecran,0, largeur_ecran//20, hauteur_ecran//20)  # setGeometry(x, y, width, height)
bouton_quitter.clicked.connect(interface.close)
bouton_quitter.raise_() # fait passer le bouton quitter en premier plan car sinon caché par le label score

bouton_start.setGeometry((largeur_ecran // 2) - largeur_ecran//10,(hauteur_ecran // 2) - hauteur_ecran//10,largeur_ecran//10,hauteur_ecran//10)
bouton_start.clicked.connect(start_match)
bouton_start.raise_()

score.setGeometry(largeur_ecran // 2, 0 , largeur_ecran//2, hauteur_ecran//2)
chrono.setGeometry(0, 0 , largeur_ecran//2, hauteur_ecran//2)


timer_match = QTimer() # Création d'un QTimer
timer = Timer(duree_match, duree_penalite, chrono, timer_match)


points=Score(score1, score2, score)
points.update_score()

timer_match.timeout.connect(timer.update_timer_match) # à chaque "tic" d'horloge exécution de la fonction update_timer



sys.exit(app.exec())