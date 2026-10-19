#Goal.py
import cv2
from PySide6.QtGui import QShortcut, QKeySequence

list_goals = []
A_Goal_Validated = True
B_Goal_Validated = True
score = [0,0]
middle = 0
foul = 0
minframecount = 1
midframecount = 5
maxframecount = 8
Drone = {}
TeamA = []
TeamB = []

#Séléction des cerceaux
def goal_creation(frame):
    global middle
    cv2.putText(frame, "Selection des cerceaux", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)
    for i in range (0, 2):
        goal_zone = cv2.selectROI("Select Goal", frame, fromCenter=False, showCrosshair=True)
        list_goals.append(goal_zone)
        cv2.destroyWindow("Select Goal")
    
    goal_x1,goal_y1,goal_w1,goal_h1 = list_goals[0]
    goal_x2,goal_y2,goal_w2,goal_h2 = list_goals[1]
    
    if goal_x1<goal_x2:
        middle = (goal_x2+goal_x1+goal_w1)//2
    else :
         middle = (goal_x1+goal_x2+goal_w2)//2

    return

def drone_initialisation(drone_id,drone_x,drone_y,team):
    global Drone
    Drone[drone_id] = {
        "x": int(drone_x),
        "y": int(drone_y),
        "team": team,
        "is_striker": False,
        "prev_x": [],
        "prev_y": [],
    }
    if team == 0:
        TeamA.append(drone_id)
    if team == 1:
        TeamB.append(drone_id)
    return


#Identification des drones
def set_team_striker():
    global Drone
    StrikerA = int(input("Donner l'ID du Striker de l'équipe A : "))
    Drone[StrikerA]["is_striker"] = True
    StrikerB = int(input("Donner l'ID du striker de l'équipe B : "))
    Drone[StrikerB]["is_striker"] = True
    print("striker set and ID ",StrikerA," : ",Drone[StrikerA]["is_striker"],",",StrikerB," : ",Drone[StrikerB]["is_striker"])
    return

#Test si le but est valide
def Test_goal(drone_x,drone_y,drone_w,drone_h,drone_id):
    global score, A_Goal_Validated, B_Goal_Validated, foul, Drone
    ValideDirection = True


    if not Drone[drone_id]["is_striker"]:
            goal_x,goal_y,goal_w,goal_h = list_goals[0]
            if (drone_x>goal_x and drone_y>goal_y and (drone_x+drone_w)<(goal_x+goal_w) and (drone_y+drone_h)<(goal_y+goal_h)):
                foul+=1
    
    elif drone_id in TeamA:
        #print("TeamA")
        goal_x,goal_y,goal_w,goal_h = list_goals[1]
        ValideDirection = valid_trajectory(drone_id)
        if (drone_x>goal_x and drone_y>goal_y and (drone_x+drone_w)<(goal_x+goal_w) and (drone_y+drone_h)<(goal_y+goal_h)):
            if A_Goal_Validated == True and ValideDirection == True:
                A_Goal_Validated = False
            else:
                foul+=1

    elif drone_id in TeamB:
        #print("TeamB")
        goal_x,goal_y,goal_w,goal_h = list_goals[0]
        ValideDirection = valid_trajectory(drone_id)
        if (drone_x>goal_x and drone_y>goal_y and (drone_x+drone_w)<(goal_x+goal_w) and (drone_y+drone_h)<(goal_y+goal_h)):
                if B_Goal_Validated == True and ValideDirection == True:
                   B_Goal_Validated = False 
                else:
                    foul+=1
        
    return


def goal_is_validated(Team):
    global  A_Goal_Validated, B_Goal_Validated, Drone,middle
    if Team == 0 and not A_Goal_Validated :
        for drone_id in TeamA:
            if Drone[drone_id]["x"]>middle:
                A_Goal_Validated = False
                return
        A_Goal_Validated = True
        score[0]+=1
        

    if Team == 1 and not B_Goal_Validated:
        for drone_id in TeamB:
            if Drone[drone_id]["x"]<middle:
                B_Goal_Validated = False
                return
        B_Goal_Validated = True
        score[1]+=1
    return

def valid_trajectory(drone_id):
    global Drone,midframecount
    
    if not Drone[drone_id]["is_striker"]:
        #print("stricker")
        return False
    
    if (len(Drone[drone_id]["prev_x"]) < midframecount) or (len(Drone[drone_id]["prev_y"]) < midframecount):
        #print("frame")
        return False
    
    curr_x,curr_y = Drone[drone_id]["x"],Drone[drone_id]["y"]
    goalA_x = list_goals[0][0]
    goalB_x = list_goals[1][0]
    n = len(Drone[drone_id]["prev_x"][:midframecount])
    dx = (n*curr_x-sum(Drone[drone_id]["prev_x"][:midframecount]))/n
    dy = (n*curr_y-sum(Drone[drone_id]["prev_y"][:midframecount]))/n
    magnitude = (dx**2 + dy**2)**0.5
    if magnitude == 0:
        DirectionVector = (0,0)
    else:
        DirectionVector = ((curr_x+dx*50/magnitude), (curr_y+dy*50/magnitude))
    scalar_product = 0
    if drone_id in TeamA:
        if goalB_x > goalA_x:
            scalar_product = DirectionVector[0]*1 + DirectionVector[1]*0
        else :
            scalar_product = DirectionVector[0]*(-1) + DirectionVector[1]*0
    
    if drone_id in TeamB:
        if goalA_x > goalB_x:
            scalar_product = DirectionVector[0]*(-1) + DirectionVector[1]*0
        else :
            scalar_product = DirectionVector[0]*1 + DirectionVector[1]*0
    return scalar_product > 0

def update_coord(x,y,drone_id):
    global Drone,maxframecount
    Drone[drone_id]["prev_x"].append(Drone[drone_id]["x"])
    Drone[drone_id]["prev_y"].append(Drone[drone_id]["y"])
    Drone[drone_id]["x"] = x
    Drone[drone_id]["y"] = y
    if len(Drone[drone_id]["prev_x"])>maxframecount+2:
            Drone[drone_id]["prev_x"].pop(0)
            Drone[drone_id]["prev_y"].pop(0)
    return
    

# Fonctions d'affichage
def draw_goals(frame):

    #But de l'équipe A
    goal_x,goal_y,goal_w,goal_h = list_goals[0]
    cv2.rectangle(frame, (goal_x, goal_y), (goal_x + goal_w, goal_y + goal_h), (255, 0, 0), 2)
    cv2.putText(frame, "Goal Team A", (goal_x, goal_y-5), cv2.FONT_HERSHEY_SIMPLEX,0.7, (255, 0, 0), 2)
    
    #But de l'équipe B
    goal_x,goal_y,goal_w,goal_h = list_goals[1]
    cv2.rectangle(frame, (goal_x, goal_y), (goal_x + goal_w, goal_y + goal_h), (0, 0, 255), 2)
    cv2.putText(frame, "Goal Team B", (goal_x, goal_y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    #Affichage du score
    cv2.putText(frame, "Score A/B " + str(score[0]) + "/" + str(score[1]), (300, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)
    return

def draw_vector(frame,drone_id):
    global Drone,maxframecount,midframecount,minframecount
    
    if (len(Drone[drone_id]["prev_x"]) < maxframecount) or (len(Drone[drone_id]["prev_y"]) < maxframecount):
            return False

    
    n1 = len(Drone[drone_id]["prev_x"][:minframecount])
    n2 = len(Drone[drone_id]["prev_x"][:midframecount])
    n3 = len(Drone[drone_id]["prev_x"][:maxframecount])
    curr_x,curr_y = Drone[drone_id]["x"],Drone[drone_id]["y"]
    
    dx1 = (n1*curr_x-sum(Drone[drone_id]["prev_x"][:minframecount]))/n1
    dy1 = (n1*curr_y-sum(Drone[drone_id]["prev_y"][:minframecount]))/n1

    dx2 = (n2*curr_x-sum(Drone[drone_id]["prev_x"][:midframecount]))/n2
    dy2 = (n2*curr_y-sum(Drone[drone_id]["prev_y"][:midframecount]))/n2

    dx3 = (n3*curr_x-sum(Drone[drone_id]["prev_x"][:maxframecount]))/n3
    dy3 = (n3*curr_y-sum(Drone[drone_id]["prev_y"][:maxframecount]))/n3

    magnitude1 = (dx1**2 + dy1**2)**0.5
    magnitude2 = (dx2**2 + dy2**2)**0.5
    magnitude3 = (dx3**2 + dy3**2)**0.5
    if magnitude1 == 0 or magnitude2 == 0 or magnitude3 == 0 :
         return
    #print("  x = ", curr_x, "  y = ", curr_y,"  dx = ", dx, "  dy = ", dy, "  coord = ",int(curr_x+dx*50/magnitude), ",", int(curr_y+dy*50/magnitude) )
    cv2.arrowedLine(frame,(curr_x,curr_y),(int(curr_x+dx1*50/magnitude1),int(curr_y+dy1*50/magnitude1)),(255,0,0), 2)
    cv2.arrowedLine(frame,(curr_x,curr_y),(int(curr_x+dx2*50/magnitude2),int(curr_y+dy2*50/magnitude2)),(0,255,0), 2)
    cv2.arrowedLine(frame,(curr_x,curr_y),(int(curr_x+dx3*50/magnitude3),int(curr_y+dy3*50/magnitude3)),(0,0,255), 2)
    return

def draw_middle(frame):
    global middle
    cv2.line(frame,(middle,0),(middle,800),(0,200,200),3)
