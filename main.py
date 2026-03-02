from fichier_test import Timer

import sys
from PySide6.QtWidgets import * #importe tous les widgets 
from PySide6.QtCore import QTimer, Qt #nécessaire Qtimer


app = QApplication(sys.argv)
interface=QWidget()                    #création fen^tre vide
interface.setWindowTitle("Interface")     # Titre de la fenêtre
interface.resize(400, 400)             # Taille de la fenêtre (largeur x hauteur)

interface.show()


timer_match = QTimer()           # Création d'un QTimer
timer_match.timeout.connect(update_timer_match) # à chaque "tic" d'horloge exécution de la fonction update_timer
timer_match.start(1000)

#timer_penalite = QTimer()           # Création d'un QTimer
#timer_penalite.timeout.connect(Tupdate_timer_penalite) # à chaque "tic" d'horloge exécution de la fonction update_timer



chrono = QLabel(interface)
chrono.setAlignment(Qt.AlignCenter)
chrono.resize(400, 400)
chrono.setStyleSheet("color:white; font-size: 40px;")  # augmente la taille d'écriture du chrono                      

















timer=Timer()
timer.validation_communication_main_fichier_test()


sys.exit(app.exec())