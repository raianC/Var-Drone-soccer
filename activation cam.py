import cv2
webcam = cv2.VideoCapture(2) # le chiffre 2 correspond à la caméra fisheye avec un fps élevé
# on créé une boucle
while(True):
    #on recupere frame par frame
    ret, frame = webcam.read()
    # on affiche le frame
    cv2.imshow('frame', frame)
    #on dit au logiciel d'attendre que la touche "q" soit pressée pour arrêter >
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
webcam.release()
cv2.destroyAllWindows()