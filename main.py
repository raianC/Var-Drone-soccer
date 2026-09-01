# A chaque fois qu'un but sera détecté il faut faire soit points.ajouter_point_equipe2() soit points.ajouter_point_equipe2() : ça détecte si on a bien un jeu en cours pour ne pas ajouter des points si on n'est pas en train de jouer
# pour la durée des sets il faut mettre dans le main le temps désiré en secondes dans la variable duree_match
# pour le temps de pénalité il faut ajouter 10 secondes soit à duree_penalite_accordee_equipe1, soit à duree_penalite_accordee_equipe2 : ce temps là sera transmis à la fin du set au timer pour exécuter ou non le temps de pénalité -> ATTENTION: erreur de la part de l'équipe 1 => +10secondes à duree_penalite_accordee_equipe2 , pas à duree_penalite_accordee_equipe1

from timer import Timer
from score import Score
from camera_live import CameraWidget
from video_bouton import VideoButton
import cv2
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer, Qt

duree_penalite_accordee_equipe1 = 0
duree_penalite_accordee_equipe2 = 0
duree_match = 8

#nombre_sets = 0
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
    timer.reset_match()
    numero_set += 1
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

    #ligne de test, à suprimer:
    if numero_set-1==1 or numero_set-1==3:
        points.ajouter_point_equipe2()

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
    points.update_sets_gagnes()

    #déconnecte uniquement si a été connecté avant
    try:
        timer_match.timeout.disconnect(timer.penalite_accordee_equipe2)
    except TypeError:
        pass

        
    if  points.test_winner()==False and numero_set-1<3: # nouveau set tant qu'il n'y a pas de gagnant et qu'on n'a pas atteint les 3 sets
    # numero_set-1 et non numero_set car numero_set est incrémenté à la fin du set et non à la fin des penalites 
    # laisser le test points.test_winner()==False avant numero_set-1<3 sinon ça ne teste pas si il y a un gagnant à la fin du 3ème set car la condition numero_set-1<3 n'est déjà pas remplie   
        bouton_start_set.setText(f"START SET {numero_set}")
        bouton_start_set.show()
        



#def choisir_2_sets():
#    global nombre_sets
#
#    nombre_sets = 2

#    bouton_2sets.hide()
#    bouton_3sets.hide()
#    texte_accueil.hide()
    
#    bouton_start_set.show()
#    chrono.show()
#    score.show()
#    score_total.show()

#    texte_score_set_en_cours.show()
#    texte_score_total_sets_precedents.show()
    
#    cam.start()


def start_game():
    #global nombre_sets

    #nombre_sets = 3

    #bouton_2sets.hide()
    #bouton_3sets.hide()
    #texte_accueil.hide()
   
    bouton_start_set.show()
    chrono.show()
    score1.show()
    score2.show()
    score_total.show()

    texte_team1.show()
    texte_team2.show()
    #texte_nb_sets_total_gagnes.show()
    #texte_score_total_sets_precedents.show()
    
    cam.start()
    btn_video.raise_button_replay()


chrono = QLabel(interface)
chrono.setAlignment(Qt.AlignCenter)
chrono.setText("0:0")
chrono.setStyleSheet(
    "color:white; font-size:40px;"
)
chrono.hide()

bouton_quitter = QPushButton("Quitter", interface)


bouton_start_set = QPushButton(f"START SET {numero_set}", interface)
bouton_start_set.hide()

bouton_start_penalite_equipe1 = QPushButton(f"START PENALITE ACCORDEE A L'EQUIPE 1", interface)
bouton_start_penalite_equipe1.hide()

bouton_start_penalite_equipe2 = QPushButton(f"START PENALITE ACCORDEE A L'EQUIPE 2", interface)
bouton_start_penalite_equipe2.hide()



score1 = QLabel(interface)
score1.setAlignment(Qt.AlignCenter)
score1.setStyleSheet(
    "color:blue; font-size:40px;"
)
score1.hide()

score2 = QLabel(interface)
score2.setAlignment(Qt.AlignCenter)
score2.setStyleSheet(
    "color:red; font-size:40px;"
)
score2.hide()

score_total = QLabel(interface)
score_total.setAlignment(Qt.AlignCenter)
score_total.setStyleSheet(
    "color:white; font-size:40px;"
)
score_total.hide()

total_sets_gagnes = QLabel(interface)
total_sets_gagnes.setAlignment(Qt.AlignCenter)
total_sets_gagnes.setStyleSheet(
    "color:white; font-size:40px;"
)
total_sets_gagnes.hide()


texte_entete = QLabel(interface)
texte_entete.setText("VAR DRONE SOCCER")
texte_entete.setAlignment(Qt.AlignCenter)
texte_entete.setStyleSheet(
    "color:white; font-size:60px; font-weight:bold;border:2px solid white;"
)

texte_team1 = QLabel(interface)
texte_team1.setText("Team 1")
texte_team1.setAlignment(Qt.AlignCenter)
texte_team1.setStyleSheet(
    "color:red; font-size:50px; font-weight:bold;"
)
texte_team1.hide()

texte_team2 = QLabel(interface)
texte_team2.setText("Team 2")
texte_team2.setAlignment(Qt.AlignCenter)
texte_team2.setStyleSheet(
    "color:blue; font-size:50px; font-weight:bold;"
)
texte_team2.hide()

texte_nb_sets_total_gagnes = QLabel(interface)
texte_nb_sets_total_gagnes.setText("Total sets gagnés")
texte_nb_sets_total_gagnes.setAlignment(Qt.AlignCenter)
texte_nb_sets_total_gagnes.setStyleSheet(
    "color:white; font-size:40px; font-weight:bold;"
)
texte_nb_sets_total_gagnes.hide()


#texte_score_total_sets_precedents = QLabel(interface)
#texte_score_total_sets_precedents.setText("Score total des sets précédents")
#texte_score_total_sets_precedents.setAlignment(Qt.AlignCenter)
#texte_score_total_sets_precedents.setStyleSheet(
#    "color:white; font-size:40px; font-weight:bold;"
#)
#texte_score_total_sets_precedents.hide()

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



# texte entete
texte_entete.setGeometry(
    0,
    0,
   largeur_ecran,
   hauteur_ecran // 6
)


# texte_team1
texte_team1.setGeometry(
    largeur_ecran // 2,        # moitié droite
    hauteur_ecran // 4,        # en haut
    largeur_ecran // 4,        # largeur moitié écran
    hauteur_ecran // 20        # petite hauteur pour titre
)

# texte_team1
texte_team2.setGeometry(
    largeur_ecran // 2+ largeur_ecran//8,          
    hauteur_ecran // 4,        # en haut
    largeur_ecran // 2,        # largeur moitié écran
    hauteur_ecran // 20        # petite hauteur pour titre
)









#texte_nb_sets_total_gagnes
texte_nb_sets_total_gagnes.setGeometry(
    largeur_ecran // 2,              # moitié droite
    hauteur_ecran // 2 + hauteur_ecran // 20,   # début du bas
    largeur_ecran // 2,
    hauteur_ecran // 15
)


#texte_score_total_sets_precedents
#texte_score_total_sets_precedents.setGeometry(
#    largeur_ecran // 2,              # moitié droite
#    hauteur_ecran // 2 + hauteur_ecran // 20,   # début du bas
#    largeur_ecran // 2,
#    hauteur_ecran // 20
#)




# Bouton START_SET
bouton_start_set.setGeometry(
    largeur_ecran-largeur_ecran // 4-largeur_ecran // 20,
    hauteur_ecran-hauteur_ecran // 10,
    largeur_ecran // 10,
    hauteur_ecran // 10
)

bouton_start_set.clicked.connect(start_set)

# Bouton START_PENALITE1
bouton_start_penalite_equipe1.setGeometry(
    largeur_ecran-largeur_ecran // 4-largeur_ecran // 12,
    hauteur_ecran-hauteur_ecran // 8,
    largeur_ecran // 6,
    hauteur_ecran // 8
)
bouton_start_penalite_equipe1.clicked.connect(start_penalite_equipe1)

# Bouton START_PENALITE2
bouton_start_penalite_equipe2.setGeometry(
    largeur_ecran-largeur_ecran // 4-largeur_ecran // 12,
    hauteur_ecran-hauteur_ecran // 8,
    largeur_ecran // 6,
    hauteur_ecran // 8
)
bouton_start_penalite_equipe2.clicked.connect(start_penalite_equipe2)



bouton_quitter.raise_()

score1.setGeometry(
    largeur_ecran // 2 + largeur_ecran//8,
    hauteur_ecran // 4,
    largeur_ecran // 2,
    hauteur_ecran // 2
)

score2.setGeometry(
    largeur_ecran // 2 ,
    hauteur_ecran // 4 ,
    largeur_ecran // 2,
    hauteur_ecran // 2
)


#score_total.setGeometry(
#    largeur_ecran // 2,
#    hauteur_ecran//2,
#    largeur_ecran // 2,
#    hauteur_ecran // 2
#)


total_sets_gagnes.setGeometry(
    largeur_ecran // 2,
    hauteur_ecran//2,
    largeur_ecran // 2,
    hauteur_ecran // 2
)


chrono.setGeometry(
    0,
    hauteur_ecran//10,
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

points = Score(score1,score2,score_total, total_sets_gagnes)

btn_video = VideoButton(interface, largeur_ecran, hauteur_ecran, "Vidéo")
btn_video.show()



cam = CameraWidget(interface ,largeur_ecran, hauteur_ecran)

start_game()
sys.exit(app.exec())