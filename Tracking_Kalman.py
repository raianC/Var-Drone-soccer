import cv2
import numpy as np

cap = cv2.VideoCapture("DualDrone1.mp4")
ret, frame = cap.read()
bbox = cv2.selectROI('Select Object', frame, False)

# Define the template image
template = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform template matching
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Draw a bounding box around the tracked object
    top_left = max_loc
    bottom_right = (top_left[0] + int(bbox[2]), top_left[1] + int(bbox[3]))
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Display the tracked object
    cv2.imshow('Tracked Object', frame)

    # Wait for a key press
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Define the initial tracking window
x, y, w, h = bbox
track_window = (x, y, w, h)
# Set up the parameters for the mean shift algorithm
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Calculate the histogram of the region of interest
    roi = hsv[y:y+h, x:x+w]
    roi_hist = cv2.calcHist([roi], [0], None, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Perform mean shift tracking
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    ret, track_window = cv2.meanShift(dst, track_window, term_crit)

    # Draw a bounding box around the tracked object
    x, y, w, h = track_window
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the tracked object
    cv2.imshow('Tracked Object', frame)

    # Wait for a key press
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Define the state-space model
dt = 1/30.0
A = np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
B = np.zeros((4, 2))
C = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
Q = np.eye(4)*0.1
R = np.eye(2)*10
x = np.array([[bbox[0]], [bbox[1]], [0], [0]])
P = np.eye(4)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Predict the next state using the state transition matrix
    x = A.dot(x) + B.dot(np.array([[np.random.normal()], [np.random.normal()]]))
    P = A.dot(P).dot(A.T) + Q

    # Calculate the measurement using the current frame
    z = np.array([[bbox[0]+bbox[2]/2], [bbox[1]+bbox[3]/2]])
    y = z - C.dot(x)
    S = C.dot(P).dot(C.T) + R
    K = P.dot(C.T).dot(np.linalg.inv(S))

    # Update the state estimate using the measurement
    x = x + K.dot(y)
    P = (np.eye(4) - K.dot(C)).dot(P)

    # Draw a bounding box around the tracked object using the state estimate
    x_, y_, w_, h_ = map(int, [x[0, 0]-bbox[2]/2, x[1, 0]-bbox[3]/2, bbox[2], bbox[3]])
    cv2.rectangle(frame, (x_, y_), (x_+w_, y_+h_), (0, 255, 0), 2)

    # Display the tracked object
    cv2.imshow('Tracked Object', frame)

    # Wait for a key press
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

