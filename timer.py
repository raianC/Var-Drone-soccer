# tkinker trop limité pour afficher plusieurs choses sur une fenêtre notamment une vidéo donc utilisation de pySide
# code inspiré du site: https://wiki.fablab.sorbonne-universite.fr/BookStack/books/logiciels/page/faire-une-interface-graphique-avec-pyside-6

#le Qtimer ne compte pas réellement le temps, il permet de lancer une action de manière périodique

# Importation des bibliothèques
import sys
from PySide6.QtWidgets import * #importe tous les widgets 
from PySide6.QtCore import QTimer, Qt #nécessaire Qtimer


temps_match=20 # création et initialisation compteur de temps
temps_penalite=15

def update_timer_match():
    global temps_match 
    temps_match -= 1
    minutes = temps_match//60 # // division entière, sans virgule
    secondes = temps_match % 60
    chrono.setText(f"{minutes}:{secondes}")
    if temps_match == 0:   # si 3 minutes atteintes
        timer_match.stop()   # on arrête le timer
        print("Temps match écoulé")
        update_timer_penalite()
        timer_penalite.start(1000)

    

def update_timer_penalite():
    chrono.setStyleSheet("color: red; font-size: 40px;")
    global temps_penalite 
    temps_penalite -= 1
    minutes = temps_penalite//60 # // division entière, sans virgule
    secondes = temps_penalite % 60
    chrono.setText(f"{minutes}:{secondes}")
    if temps_penalite == 0:   # si 3 minutes atteintes
        timer_penalite.stop()   # on arrête le timer
        print("Temps pénalité écoulé")



app = QApplication(sys.argv)
fenetre_timer=QWidget()                    #création fen^tre vide
fenetre_timer.setWindowTitle("Timer")     # Titre de la fenêtre
fenetre_timer.resize(400, 400)             # Taille de la fenêtre (largeur x hauteur)





timer_match = QTimer()           # Création d'un QTimer
timer_match.timeout.connect(update_timer_match) # à chaque "tic" d'horloge exécution de la fonction update_timer
timer_match.start(1000)

timer_penalite = QTimer()           # Création d'un QTimer
timer_penalite.timeout.connect(update_timer_penalite) # à chaque "tic" d'horloge exécution de la fonction update_timer



chrono = QLabel("3:0", fenetre_timer)
chrono.setAlignment(Qt.AlignCenter)
chrono.resize(400, 400)
chrono.setStyleSheet("color:white; font-size: 40px;")  # augmente la taille d'écriture du chrono                      








fenetre_timer.show()  

# Lancer la boucle principale
sys.exit(app.exec())

