import cv2

#récupération de la video, /!\ la sortie camera
webcam = cv2.VideoCapture(2)

#test de la camera, q pour sortir
while True:
    ret, frame = webcam.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyWindow("frame")

#Selection des objets a tracker, q pour sortir
list_obj = []
nb_obj = 0
list_track = []
list_succ = []

tot_obj = int(input("Select the number of object you want"))
for i in range (0, tot_obj):
    object = cv2.selectROI("Select Object to Track", frame, fromCenter=False, showCrosshair=True)
    list_obj.append(object)
    cv2.destroyWindow("Select Object to Track")
    nb_obj += 1
    print(object)
    if cv2.waitKey(1) & 0xFF == ord('q') or nb_obj == 4:
        break

for object in list_obj:
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, object)
    list_track.append(tracker)

#renvois de la vidéo avec l'objet tracké :
while True:
    ret, frame = webcam.read()
    if not ret:
        print("ca break")
        break

    nb_obj = 0
    for tracker in list_track:
        success, box = tracker.update(frame)

        if success:
            # Draw bounding box
            x, y, w, h = [int(v) for v in box]
            print("objet n°", nb_obj, " coord", x, y,)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking obect " + str(nb_obj), (10, 30 + 20*nb_obj), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
            text = "Object" + str(nb_obj)
            cv2.putText(frame, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Lost object " + str(nb_obj), (10, 30 + 20*nb_obj), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)
        nb_obj +=1
                
            # Show result
        cv2.imshow("Object Tracking", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break





webcam.release()
cv2.destroyAllWindows()