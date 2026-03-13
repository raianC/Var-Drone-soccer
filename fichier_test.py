from PySide6.QtWidgets import * #importe tous les widgets 






class Timer(QWidget):
    
    
    def __init__(self, duree_match, chrono, timer_match):
        super().__init__()

        self.duree_match = duree_match
        self.chrono = chrono
        self.timer_match = timer_match


    def update_timer_match(self):
        self.duree_match -= 1
        minutes = self.duree_match//60 # // division entière, sans virgule
        secondes = self.duree_match % 60
        self.chrono.setStyleSheet("color:white; font-size:40px; border:2px solid white;")
        self.chrono.setText(f"{minutes}:{secondes}")
        
        print("Tic")
        if self.duree_match == 0:   # si 3 minutes atteintes
            self.timer_match.stop()   # on arrête le timer
            print("Temps match écoulé")
            #update_timer_penalite()
            # timer_penalite.start(1000)

    

























#def update_timer_penalite():
#    chrono.setStyleSheet("color: red; font-size: 40px;")
#    global temps_penalite 
#    temps_penalite -= 1
#    minutes = temps_penalite//60 # // division entière, sans virgule
#    secondes = temps_penalite % 60
#    chrono.setText(f"{minutes}:{secondes}")
#    if temps_penalite == 0:   # si 3 minutes atteintes
#        timer_penalite.stop()   # on arrête le timer
#        print("Temps pénalité écoulé")