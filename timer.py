from PySide6.QtWidgets import * #importe tous les widgets 






class Timer(QWidget):
    
    
    def __init__(self, duree_match, chrono, timer_match, fin_set, fin_penalite_accordee_equipe1,fin_penalite_accordee_equipe2):
        super().__init__()

        self.duree_match = duree_match
        self.chrono = chrono
        self.timer_match = timer_match
        
        self.fin_set = fin_set
        self.fin_penalite_accordee_equipe1=fin_penalite_accordee_equipe1
        self.fin_penalite_accordee_equipe2=fin_penalite_accordee_equipe2

        self.duree_match_initiale = duree_match # utile pour ne pas repartir au set suivant avec duree_match=0

        self.duree_penalite_accordee_equipe1 = 0
        self.duree_penalite_accordee_equipe2 = 0 
    

    def update_timer_match(self):
        
        self.duree_match -= 1

        minutes = self.duree_match//60 # // division entière, sans virgule
        secondes = self.duree_match % 60

        self.chrono.setStyleSheet("color:white; font-size:40px;")
        self.chrono.setText(f"{minutes}:{secondes}")
        
        if self.duree_match <= 0 :   # si la fin du temps de match atteint
            self.duree_match = 0
            print("Temps match écoulé")
            self.stop_match()
            self.fin_set() 

    def penalite_accordee_equipe1 (self):
            if self.duree_penalite_accordee_equipe1 <= 0 :   # si fin du temps de pénalités atteint
                self.duree_penalite_accordee_equipe1 = 0
                self.stop_match()   # on arrête le timer
                print("Temps pénalité accordé à l'équipe 1 écoulé")
                self.fin_penalite_accordee_equipe1()
                return
            
            self.duree_penalite_accordee_equipe1 -= 1
            
            minutes = self.duree_penalite_accordee_equipe1//60 # // division entière, sans virgule
            secondes = self.duree_penalite_accordee_equipe1 % 60

            self.chrono.setStyleSheet("color: red; font-size: 40px; border:2px solid white;")
            self.chrono.setText(f"{minutes}:{secondes}")
            
            

    def penalite_accordee_equipe2 (self):
         
        if self.duree_penalite_accordee_equipe2 <= 0:   # si fin du temps de pénalités atteint
            self.duree_penalite_accordee_equipe2 = 0
            self.stop_match()   # on arrête le timer
            print("Temps pénalité accordé à l'équipe 2 écoulé")
            self.fin_penalite_accordee_equipe2()
            return

        self.duree_penalite_accordee_equipe2 -= 1
            
        minutes = self.duree_penalite_accordee_equipe2//60 # // division entière, sans virgule
        secondes = self.duree_penalite_accordee_equipe2 % 60

        self.chrono.setStyleSheet("color: red; font-size: 40px; border:2px solid white;")
        self.chrono.setText(f"{minutes}:{secondes}")
            
        


    def stop_match(self):
        self.timer_match.stop()

    def reset_match(self):
        self.duree_match = self.duree_match_initiale