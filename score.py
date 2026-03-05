import sys
# commande d'installation de PySide6 : pip install PySide6

from PySide6.QtWidgets import * #importe tous les widgets 
from PySide6.QtCore import Qt

score1=3
score2=2

app = QApplication(sys.argv)
fenetre = QWidget()                    #création fen^tre vide
fenetre.setWindowTitle("Score")     # Titre de la fenêtre
fenetre.resize(400, 400)             # Taille de la fenêtre (largeur x hauteur)



score = QLabel(fenetre)
score.setAlignment(Qt.AlignTop)
score.resize(400, 400)
score.setStyleSheet("color:white; font-size: 40px;")  # augmente la taille d'écriture du chrono                      






def affichage_score():
    score.setText(f"Equipe 1:{score1}/ Equipe 2: {score2}")
    


affichage_score()
fenetre.show()  

# Lancer la boucle principale
sys.exit(app.exec())
