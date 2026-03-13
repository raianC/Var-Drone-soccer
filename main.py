from fichier_test import Timer

import sys
from PySide6.QtWidgets import * #importe tous les widgets 
from PySide6.QtCore import QTimer, Qt #nécessaire Qtimer




duree_match=20

app = QApplication(sys.argv)
interface=QWidget()                    #création fenêtre vide
interface.setWindowTitle("Interface")     # Titre de la fenêtre
#interface.resize(400, 400)             # Taille de la fenêtre (largeur x hauteur)






chrono = QLabel(interface)
chrono.setAlignment(Qt.AlignCenter)
chrono.resize(400, 400)
chrono.setStyleSheet("color:white; font-size: 40px;")  # augmente la taille d'écriture du chrono                      

bouton_quitter = QPushButton("Quitter", interface)


interface.showFullScreen() #montre la fenêtre (Attention, montrer après avoir créé les labels)

largeur_ecran = interface.width()
hauteur_ecran = interface.height()


bouton_quitter.setGeometry(largeur_ecran-60,10, 55, 55)  # setGeometry(x, y, width, height)
bouton_quitter.clicked.connect(interface.close)


timer_match = QTimer() # Création d'un QTimer
timer = Timer(duree_match, chrono, timer_match)



timer_match.timeout.connect(timer.update_timer_match) # à chaque "tic" d'horloge exécution de la fonction update_timer
timer_match.start(1000)



sys.exit(app.exec())