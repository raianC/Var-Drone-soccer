from PySide6.QtWidgets import * #importe tous les widgets 

class Timer(QWidget):
    
    def update_timer_match(self):
    temps_match -= 1
    minutes = temps_match//60 # // division entière, sans virgule
    secondes = temps_match % 60
    chrono.setText(f"{minutes}:{secondes}")
    if temps_match == 0:   # si 3 minutes atteintes
        timer_match.stop()   # on arrête le timer
        print("Temps match écoulé")
        update_timer_penalite()
        timer_penalite.start(1000)

    

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