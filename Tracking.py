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

#Selection de l'objet a tracker, Entrée pour sortir
object = cv2.selectROI("Select Object to Track", frame, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select Object to Track")

tracker = cv2.TrackerCSRT_create()
tracker.init(frame, object)

#renvois de la vidéo avec l'objet tracké :
while True:
    ret, frame = webcam.read()
    if not ret:
        print("ca break")
        break

    success, box = tracker.update(frame)

    if success:
        # Draw bounding box
        x, y, w, h = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Lost", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 2)
                
            # Show result
    cv2.imshow("Object Tracking", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break





webcam.release()
cv2.destroyAllWindows()