from PySide6.QtWidgets import * #importe tous les widgets 

class Score():
    
    def __init__(self, score, score_total):
        super().__init__()
        
        self.score = score
        self.score_total = score_total
        
        self.score1 = 0
        self.score2 = 0

        self.score1_total = 0
        self.score2_total = 0

        self.set_en_cours = False
        self.penalite_en_cours = False



    def update_score(self):
        self.score.setText( f"Equipe 1 vs Equipe 2\n"
            f"{self.score1}                     {self.score2}")
    
    def update_score_total(self):

        self.score_total.setText( f"Equipe 1 vs Equipe 2\n"
            f"{self.score1_total}                     {self.score2_total}")
    
    
    def ajouter_set_au_total(self):

        self.score1_total += self.score1 # ajoute le score du set actuel au score des sets précédents
        self.score2_total += self.score2

        self.update_score_total()
    
    
    
    
    def start_set(self):
        
        self.score1=0
        self.score2=0

        self.set_en_cours=True

        self.update_score()


    def fin_set(self):

        self.set_en_cours=False

    def start_penalite(self):
        self.penalite_en_cours = True

    def fin_penalite(self):
        self.penalite_en_cours=False
    
    def ajouter_point_equipe1(self):

        if self.set_en_cours or self.penalite_en_cours:
            self.score1 += 1

        self.update_score()

    def ajouter_point_equipe2(self):

        if self.set_en_cours or self.penalite_en_cours:
            self.score2 += 1

        self.update_score()