import fichier_test#, timer, score 

import sys
from PySide6.QtWidgets import * #importe tous les widgets 
from PySide6.QtCore import QTimer, Qt #nécessaire Qtimer


app = QApplication(sys.argv)
interface=QWidget()                    #création fen^tre vide
interface.setWindowTitle("Interface")     # Titre de la fenêtre
interface.resize(400, 400)             # Taille de la fenêtre (largeur x hauteur)

interface.show()


fichier_test.validation_communication_main_fichier_test()


sys.exit(app.exec())