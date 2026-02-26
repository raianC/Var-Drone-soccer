# tkinker trop limité pour afficher plusieurs choses sur une fenêtre notamment une vidéo donc utilisation de pySide
# code inspiré du site: https://wiki.fablab.sorbonne-universite.fr/BookStack/books/logiciels/page/faire-une-interface-graphique-avec-pyside-6

# Importation des bibliothèques
import sys
from PySide6.QtWidgets import * #importe tous les widgets 


temps=0 # création et initialisation compteur de temps

def update_timer():
    global temps 
    temps += 1
    


app = QApplication(sys.argv)
fenetre_timer=QWidget()                    #création fen^tre vide
fenetre_timer.setWindowTitle("Timer")     # Titre de la fenêtre
fenetre_timer.resize(400, 400)             # Taille de la fenêtre (largeur x hauteur)
fenetre_timer.show()                        # Affiche la fenêtre



timer = QTimer()           # Création d'un QTimer
timer.timeout.connect(update_timer) 
timer.start(1000) 






# Lancer la boucle principale
sys.exit(app.exec())

