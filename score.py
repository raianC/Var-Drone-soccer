from PySide6.QtWidgets import * #importe tous les widgets 

class Score():
    
    def __init__(self, score1, score2, score):
        super().__init__()
        
        self.score1=score1
        self.score2=score2
        self.score=score


    def update_score(self):
        self.score.setText( f"Equipe 1 vs Equipe 2\n"
            f"{self.score1}                     {self.score2}")
    