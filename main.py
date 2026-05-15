# A chaque fois qu'un but sera détecté il faut faire soit points.ajouter_point_equipe2() soit points.ajouter_point_equipe2() : ça détecte si on a bien un jeu en cours pour ne pas ajouter des points si on n'est pas en train de jouer
# pour la durée des sets il faut mettre dans le main le temps désiré en secondes dans la variable duree_match
# pour le temps de pénalité il faut ajouter 10 secondes soit à duree_penalite_accordee_equipe1, soit à duree_penalite_accordee_equipe2 : ce temps là sera transmis à la fin du set au timer pour exécuter ou non le temps de pénalité -> ATTENTION: erreur de la part de l'équipe 1 => +10secondes à duree_penalite_accordee_equipe2 , pas à duree_penalite_accordee_equipe1

from timer import Timer
from score import Score

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer, Qt

duree_penalite_accordee_equipe1 = 0
duree_penalite_accordee_equipe2 = 0
duree_match = 8

nombre_sets = 0
numero_set = 1

app = QApplication(sys.argv)

interface = QWidget()
interface.setWindowTitle("Interface")

def start_set():
    global duree_penalite_accordee_equipe1
    global duree_penalite_accordee_equipe2

    duree_penalite_accordee_equipe1=0  # pénalités remises à 0 pour chaque début de match
    duree_penalite_accordee_equipe2=0

    timer_match.start(1000)
    bouton_start_set.hide()
    timer_match.timeout.connect(timer.update_timer_match)

    points.start_set()


def fin_set():
    timer_match.timeout.disconnect(timer.update_timer_match)
    global numero_set
    numero_set += 1
    timer.reset_match()

    points.fin_set()

    #juste pour les tests avant la partie de Dorian
    global duree_penalite_accordee_equipe1
    duree_penalite_accordee_equipe1=5
    global duree_penalite_accordee_equipe2
    duree_penalite_accordee_equipe2=5



    if duree_penalite_accordee_equipe1 > 0:
        bouton_start_penalite_equipe1.show()
    else:
        fin_penalite_accordee_equipe1()

def start_penalite_equipe1():
    points.start_penalite()

    timer.duree_penalite_accordee_equipe1=duree_penalite_accordee_equipe1
    
    bouton_start_penalite_equipe1.hide()
    timer_match.start(1000)
    timer_match.timeout.connect(timer.penalite_accordee_equipe1)

def start_penalite_equipe2():
    points.start_penalite()
    
    timer.duree_penalite_accordee_equipe2=duree_penalite_accordee_equipe2
  
    bouton_start_penalite_equipe2.hide()
    timer_match.start(1000)
    timer_match.timeout.connect(timer.penalite_accordee_equipe2)


def fin_penalite_accordee_equipe1():
    points.fin_penalite()
   
    #déconnecte uniquement si a été connecté avant
    try:
        timer_match.timeout.disconnect(timer.penalite_accordee_equipe1)
    except TypeError:
        pass

    if duree_penalite_accordee_equipe2 > 0:
        bouton_start_penalite_equipe2.show()
    else:
        fin_penalite_accordee_equipe2()

def fin_penalite_accordee_equipe2():
    points.fin_penalite()
    points.ajouter_set_au_total()


    #déconnecte uniquement si a été connecté avant
    try:
        timer_match.timeout.disconnect(timer.penalite_accordee_equipe2)
    except TypeError:
        pass

        
    if(numero_set<nombre_sets+1):
        bouton_start_set.setText(f"START SET {numero_set}")
        bouton_start_set.show()


def choisir_2_sets():
    global nombre_sets

    nombre_sets = 2

    bouton_2sets.hide()
    bouton_3sets.hide()
    texte_accueil.hide()
    
    bouton_start_set.show()
    chrono.show()
    score.show()
    score_total.show()

    texte_score_set_en_cours.show()
    texte_score_total_sets_precedents.show()


def choisir_3_sets():
    global nombre_sets

    nombre_sets = 3

    bouton_2sets.hide()
    bouton_3sets.hide()
    texte_accueil.hide()
   
    bouton_start_set.show()
    chrono.show()
    score.show()
    score_total.show()

    texte_score_set_en_cours.show()
    texte_score_total_sets_precedents.show()


chrono = QLabel(interface)
chrono.setAlignment(Qt.AlignCenter)
chrono.setText("0:0")
chrono.setStyleSheet(
    "color:white; font-size:40px;border:2px solid white;"
)
chrono.hide()

bouton_quitter = QPushButton("Quitter", interface)


bouton_start_set = QPushButton(f"START SET {numero_set}", interface)
bouton_start_set.hide()

bouton_start_penalite_equipe1 = QPushButton(f"START PENALITE ACCORDEE A L'EQUIPE 1", interface)
bouton_start_penalite_equipe1.hide()

bouton_start_penalite_equipe2 = QPushButton(f"START PENALITE ACCORDEE A L'EQUIPE 2", interface)
bouton_start_penalite_equipe2.hide()

bouton_2sets = QPushButton("2 sets", interface)
bouton_3sets = QPushButton("3 sets", interface)

score = QLabel(interface)
score.setAlignment(Qt.AlignCenter)
score.setStyleSheet(
    "color:white; font-size:40px;border:2px solid white;"
)
score.hide()


score_total = QLabel(interface)
score_total.setAlignment(Qt.AlignCenter)
score_total.setStyleSheet(
    "color:white; font-size:40px;border:2px solid white;"
)
score_total.hide()


texte_accueil = QLabel(interface)
texte_accueil.setText("Bonjour !\nCombien de sets voulez-vous réaliser ?")
texte_accueil.setAlignment(Qt.AlignCenter)
texte_accueil.setStyleSheet(
    "color:white; font-size:40px; font-weight:bold;"
)

texte_score_set_en_cours = QLabel(interface)
texte_score_set_en_cours.setText("Score du set en cours")
texte_score_set_en_cours.setAlignment(Qt.AlignCenter)
texte_score_set_en_cours.setStyleSheet(
    "color:white; font-size:40px; font-weight:bold;"
)
texte_score_set_en_cours.hide()

texte_score_total_sets_precedents = QLabel(interface)
texte_score_total_sets_precedents.setText("Score total des set précédents")
texte_score_total_sets_precedents.setAlignment(Qt.AlignCenter)
texte_score_total_sets_precedents.setStyleSheet(
    "color:white; font-size:40px; font-weight:bold;"
)
texte_score_total_sets_precedents.hide()

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


# texte_score_set_en_cours
texte_score_set_en_cours.setGeometry(
    largeur_ecran // 2,          # moitié droite
    hauteur_ecran // 20,        # en haut
    largeur_ecran // 2,         # largeur moitié écran
    hauteur_ecran // 20         # petite hauteur pour titre
)

#texte_score_total_sets_precedents
texte_score_total_sets_precedents.setGeometry(
    largeur_ecran // 2,              # moitié droite
    hauteur_ecran // 2 + hauteur_ecran // 20,   # début du bas
    largeur_ecran // 2,
    hauteur_ecran // 20
)


# Bouton START_SET
bouton_start_set.setGeometry(
    (largeur_ecran // 2) - largeur_ecran // 10,
    (hauteur_ecran // 2) - hauteur_ecran // 10,
    largeur_ecran // 10,
    hauteur_ecran // 10
)

bouton_start_set.clicked.connect(start_set)

# Bouton START_PENALITE1
bouton_start_penalite_equipe1.setGeometry(
    (largeur_ecran // 2) - largeur_ecran // 6,
    (hauteur_ecran // 2) - hauteur_ecran // 8,
    largeur_ecran // 6,
    hauteur_ecran // 8
)
bouton_start_penalite_equipe1.clicked.connect(start_penalite_equipe1)

# Bouton START_PENALITE2
bouton_start_penalite_equipe2.setGeometry(
    (largeur_ecran // 2) - largeur_ecran // 6,
    (hauteur_ecran // 2) - hauteur_ecran // 8,
    largeur_ecran // 6,
    hauteur_ecran // 8
)
bouton_start_penalite_equipe2.clicked.connect(start_penalite_equipe2)



bouton_quitter.raise_()

score.setGeometry(
    largeur_ecran // 2,
    0,
    largeur_ecran // 2,
    hauteur_ecran // 2
)

score_total.setGeometry(
    largeur_ecran // 2,
    hauteur_ecran//2,
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
    chrono,
    timer_match,
    fin_set,
    fin_penalite_accordee_equipe1,
    fin_penalite_accordee_equipe2

)

points = Score(score,score_total)










sys.exit(app.exec())