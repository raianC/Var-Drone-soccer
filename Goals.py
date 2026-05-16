#Goal.py
import cv2

list_goals = []
A_Valid_goal = True
B_Valid_goal = True
score = [0,0]
StrikerA = 0
StrikerB = 0

#Séléction des cerceaux
def GoalCreation(frame):
    for i in range (0, 2):
        goal_zone = cv2.selectROI("Select Goal", frame, fromCenter=False, showCrosshair=True)
        list_goals.append(goal_zone)
        cv2.destroyWindow("Select Goal")
    return

#Identification des drones
def set_team_Striker():
    global StrikerA,StrikerB
    StrikerA = int(input("Donner l'ID du Striker de l'équipe A : "))
    StrikerB = int(input("Donner l'ID du striker de l'équipe B : "))
    return

#Test si le but est valide
def test_goal(drone_x,drone_y,drone_w,drone_h,drone_ID):
    global score, A_Valid_goal, B_Valid_goal
    if drone_ID == StrikerA:
        goal_x,goal_y,goal_w,goal_h = list_goals[1]
        if (drone_x>goal_x and drone_y>goal_y and (drone_x+drone_w)<(goal_x+goal_w) and (drone_y+drone_h)<(goal_y+goal_h)) and A_Valid_goal:
            score[0]+=1
            A_Valid_goal = False

    if drone_ID == StrikerB:
        goal_x,goal_y,goal_w,goal_h = list_goals[0]
        if (drone_x>goal_x and drone_y>goal_y and (drone_x+drone_w)<(goal_x+goal_w) and (drone_y+drone_h)<(goal_y+goal_h)) and B_Valid_goal:
            score[1]+=1
            B_Valid_goal = False
    return

def DrawGoals(frame):

    #But de l'équipe A
    goal_x,goal_y,goal_w,goal_h = list_goals[0]
    cv2.rectangle(frame, (goal_x, goal_y), (goal_x + goal_w, goal_y + goal_h), (255, 0, 0), 2)
    cv2.putText(frame, "Goal Team A", (goal_x, goal_y-5), cv2.FONT_HERSHEY_SIMPLEX,0.7, (255, 0, 0), 2)
    
    #But de l'équipe B
    goal_x,goal_y,goal_w,goal_h = list_goals[1]
    cv2.rectangle(frame, (goal_x, goal_y), (goal_x + goal_w, goal_y + goal_h), (0, 0, 255), 2)
    cv2.putText(frame, "Goal Team B", (goal_x, goal_y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return

def Goal_is_possible(Team):
    global  A_Valid_goal, B_Valid_goal
    if Team == 1:
        A_Valid_goal = True
    if Team == 2:
        B_Valid_goal = True
    return

