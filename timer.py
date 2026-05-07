from PySide6.QtWidgets import * #importe tous les widgets 






class Timer(QWidget):
    
    
    def __init__(self, duree_match, duree_penalite_accordee_equipe1,duree_penalite_accordee_equipe2 , chrono, timer_match):
        super().__init__()

        self.duree_match = duree_match
        self.chrono = chrono
        self.timer_match = timer_match
        self.duree_penalite_accordee_equipe1 = duree_penalite_accordee_equipe1
        self.duree_penalite_accordee_equipe2 = duree_penalite_accordee_equipe2
        
        self.mode="match"

    def update_timer_match(self):
        
        if self.mode=="match":
            self.duree_match -= 1

            minutes = self.duree_match//60 # // division entière, sans virgule
            secondes = self.duree_match % 60

            self.chrono.setStyleSheet("color:white; font-size:40px; border:2px solid white;")
            self.chrono.setText(f"{minutes}:{secondes}")
        
            if self.duree_match == 0:   # si la fin du temps de match atteint
                print("Temps match écoulé")
                self.mode="penalite"


        elif self.mode=="penalite":  # on met elif à la palce de if car cela permet de passer à ce bloc si le premier if est faux
        # sans le elif, quand on passe en mode "penalite" on perd une seconde car sur le même "tic" d'horloge on va rentrer dans la partie penalité
            self.duree_penalite_accordee_equipe1 -= 1
            
            minutes = self.duree_penalite_accordee_equipe1//60 # // division entière, sans virgule
            secondes = self.duree_penalite_accordee_equipe1 % 60

            self.chrono.setStyleSheet("color: red; font-size: 40px; border:2px solid white;")
            self.chrono.setText(f"{minutes}:{secondes}")
            
            if self.duree_penalite_accordee_equipe1 == 0:   # si fin du temps de pénalités atteint
                self.timer_match.stop()   # on arrête le timer
                print("Temps pénalité accordé à l'équipe 1 écoulé")