from PySide6.QtWidgets import * #importe tous les widgets 

class Score():
    
    def __init__(self, score1, score2, score_total, total_sets_gagnes1, total_sets_gagnes2):
        super().__init__()
        
        self.score1_label = score1
        self.score2_label = score2
        self.score_total = score_total
        self.total_sets_gagnes1_label = total_sets_gagnes1
        self.total_sets_gagnes2_label = total_sets_gagnes2
        
        self.score1 = 0
        self.score2 = 0

        self.score1_total = 0
        self.score2_total = 0

        self.set_en_cours = False
        self.penalite_en_cours = False

        self.sets_gagnes1 = 0
        self.sets_gagnes2 = 0



    def update_score(self):
        self.score1_label.setText(f"{self.score1}")
        self.score2_label.setText(f"{self.score2}")

        
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



    def update_sets_gagnes(self):

        if self.score1>self.score2:
            self.sets_gagnes1+=1

        if self.score1<self.score2:
            self.sets_gagnes2+=1

        self.total_sets_gagnes1_label.setText(f"Sets won: "  f"{self.sets_gagnes1}")
        self.total_sets_gagnes2_label.setText(f"Sets won: "  f"{self.sets_gagnes2}")


    def test_winner(self):
        if self.sets_gagnes1==2:
            print("Equipe 1 gagnante")
            return True
            
        if self.sets_gagnes2==2:
            print("Equipe 2 gagnante")
            return True 
            
        else:
            print("pas encore de gagnant")
            return False