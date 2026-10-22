
import cv2
import numpy as np
import os

# ==========================================
# CONFIGURATION
# ==========================================

CAMERA_ID = 4              # Webcam : essaie 0 ou 1
CHECKERBOARD = (8, 6)      # Coins interieurs : colonnes, lignes
SQUARE_SIZE = 80.0         # Taille d'une case en mm
OUTPUT_FILE = "calib.yml"
SAVE_FOLDER = "calibration"

os.makedirs(SAVE_FOLDER, exist_ok=True)

# ==========================================
# INITIALISATION CAMERA
# ==========================================

cap = cv2.VideoCapture(CAMERA_ID)

if not cap.isOpened():
    raise RuntimeError(
        f"Impossible d'ouvrir la camera {CAMERA_ID}. "
        "Essaie CAMERA_ID = 1."
    )

# Resolution demandee (facultatif)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.01
)

objp = np.zeros(
    (1, CHECKERBOARD[0] * CHECKERBOARD[1], 3),
    dtype=np.float64
)

objp[0, :, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objp *= SQUARE_SIZE

objpoints = []
imgpoints = []

image_size = None
saved_count = 0

print("=== CALIBRATION CAMERA EN LIVE ===")
print("C : capturer une image si le damier est detecte")
print("K : lancer la calibration")
print("Q ou ESC : quitter")

# ==========================================
# BOUCLE LIVE
# ==========================================

while True:
    ret, frame = cap.read()

    if not ret:
        print("Erreur : impossible de lire la camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if image_size is None:
        image_size = gray.shape[::-1]

    found, corners = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH
        | cv2.CALIB_CB_NORMALIZE_IMAGE
    )

    display = frame.copy()

    if found and corners is not None:
        corners_refined = cv2.cornerSubPix(
            gray,
            corners,
            (5, 5),
            (-1, -1),
            criteria
        )

        cv2.drawChessboardCorners(
            display,
            CHECKERBOARD,
            corners_refined,
            True
        )

        cv2.putText(
            display,
            "DAMI ER DETECTE - C pour capturer".replace("DAMI ER", "DAMIER"),
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    else:
        corners_refined = None
        cv2.putText(
            display,
            "Damier non detecte",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    cv2.putText(
        display,
        f"Images capturees : {saved_count}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    cv2.imshow("Calibration LIVE", display)

    key = cv2.waitKey(1) & 0xFF

    # Capturer une vue valide
    if key == ord('c'):
        if not found or corners_refined is None:
            print("Capture refusee : damier non detecte.")
            continue

        pts = corners_refined.reshape(-1, 2)

        if (
            len(pts) != CHECKERBOARD[0] * CHECKERBOARD[1]
            or not np.isfinite(pts).all()
        ):
            print("Capture refusee : points invalides.")
            continue

        # Eviter les images de resolution differente
        if image_size != gray.shape[::-1]:
            print("Capture refusee : resolution differente.")
            continue

        objpoints.append(objp.copy())
        imgpoints.append(
            pts.reshape(1, -1, 2).astype(np.float64)
        )

        filename = os.path.join(
            SAVE_FOLDER, f"image_{saved_count:02d}.jpg"
        )
        cv2.imwrite(filename, frame)

        saved_count += 1
        print(f"Image capturee : {filename}")

    # Lancer la calibration
    elif key == ord('k'):
        if len(objpoints) < 8:
            print(
                f"Il faut au moins 8 images variees. "
                f"Actuellement : {len(objpoints)}"
            )
            continue

        # Sortir de la boucle pour calibrer
        break

    elif key == ord('q') or key == 27:
        print("Arret demande.")
        cap.release()
        cv2.destroyAllWindows()
        raise SystemExit

cap.release()
cv2.destroyAllWindows()

# ==========================================
# CALIBRATION FISHEYE
# ==========================================



# objpoints, imgpoints et image_size doivent deja etre definis

# ==========================================
# FILTRAGE DES VUES ABERRANTES
# Apres la premiere calibration fisheye
# ==========================================


def calibrate_and_check(objpoints, imgpoints, image_size):
    if len(objpoints) != len(imgpoints) or len(objpoints) < 8:
        print("Pas assez de vues ou tableaux incompatibles.")
        return False

    K = np.eye(3, dtype=np.float64)
    D = np.zeros((4, 1), dtype=np.float64)

    flags = (
        cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC
        | cv2.fisheye.CALIB_FIX_SKEW
    )

    try:
        rms, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
            objpoints,
            imgpoints,
            image_size,
            K,
            D,
            None,
            None,
            flags,
            (
                cv2.TERM_CRITERIA_EPS
                + cv2.TERM_CRITERIA_MAX_ITER,
                200,
                1e-7
            )
        )

    except cv2.error as e:
        print("Echec de la calibration fisheye :")
        print(e)
        return False

    errors = []

    for i in range(len(objpoints)):
        projected, _ = cv2.fisheye.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], K, D
        )

        observed = imgpoints[i].reshape(-1, 2)
        projected = projected.reshape(-1, 2)

        error = np.sqrt(
            np.mean(np.sum((observed - projected) ** 2, axis=1))
        )
        errors.append(error)

    print("RMS :", rms)
    print("Erreur moyenne :", np.mean(errors))
    print("Erreur maximale :", np.max(errors))

    if not np.isfinite(K).all() or not np.isfinite(D).all():
        print("Parametres de calibration invalides.")
        return False

    fs = cv2.FileStorage("calib.yml", cv2.FILE_STORAGE_WRITE)
    fs.write("K", K)
    fs.write("D", D)
    fs.write("image_width", image_size[0])
    fs.write("image_height", image_size[1])
    fs.release()

    print("Calibration sauvegardee dans calib.yml")
    return True


# Appel de la fonction
success = calibrate_and_check(
    objpoints, imgpoints, image_size
)

if not success:
    print("Aucun nouveau fichier de calibration valide n'a ete produit.")
