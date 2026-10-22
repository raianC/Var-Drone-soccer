
import cv2
import numpy as np
import glob
import os

# -----------------------------
# Configuration
# -----------------------------

CHECKERBOARD = (6, 8)  # Coins interieurs : colonnes, lignes
SQUARE_SIZE =80.0     # Taille d'une case en mm
IMAGE_FOLDER = "C:\\Users\\raian\\Documents\\GitHub\\Var-Drone-soccer\\calibration"

# Critere d'affinement des coins
criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.01
)

# -----------------------------
# Points 3D de la mire
# -----------------------------

objp = np.zeros(
    (1, CHECKERBOARD[0] * CHECKERBOARD[1], 3),
    dtype=np.float64
)

objp[0, :, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objp *= SQUARE_SIZE

objpoints = []  # Points 3D
imgpoints = []  # Points 2D

image_size = None

# -----------------------------
# Lecture des images
# -----------------------------

if not os.path.isdir(IMAGE_FOLDER):
    raise FileNotFoundError(
        f"Dossier introuvable : {IMAGE_FOLDER}"
    )
    
images=glob.glob("C:\\Users\\raian\\Documents\\GitHub\\Var-Drone-soccer\\calibration\\*.jpg")

if not images:
    raise RuntimeError(
        f"Aucune image trouvee dans {IMAGE_FOLDER}"
    )

for fname in sorted(images):
    img = cv2.imread(fname)

    if img is None:
        print(f"Image illisible : {fname}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if image_size is None:
        image_size = gray.shape[::-1]

    if gray.shape[::-1] != image_size:
        print(f"Image ignoree (taille differente) : {fname}")
        continue

    # Detection du damier
    found, corners = cv2.findChessboardCorners(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_ADAPTIVE_THRESH
        + cv2.CALIB_CB_NORMALIZE_IMAGE
    )

    if not found or corners is None:
        print(f"Damier non detecte : {fname}")
        continue

    # Affinement subpixel
    corners = cv2.cornerSubPix(
        gray,
        corners,
        (5, 5),
        (-1, -1),
        criteria
    )

    corners = corners.reshape(-1, 2)

    # Verification des points
    if (
        len(corners) != CHECKERBOARD[0] * CHECKERBOARD[1]
        or not np.isfinite(corners).all()
    ):
        print(f"Points invalides : {fname}")
        continue

    # Accepter uniquement les images avec des coins valides
    imgpoints.append(corners.reshape(1, -1, 2).astype(np.float64))
    objpoints.append(objp.copy())

    print(f"Image acceptee : {fname}")

    display = img.copy()
    cv2.drawChessboardCorners(
        display, CHECKERBOARD, corners.reshape(-1, 1, 2), True
    )
    cv2.imshow("Detection du damier", display)
    cv2.waitKey(200)

cv2.destroyAllWindows()

# -----------------------------
# Verification avant calibration
# -----------------------------

print(f"\nImages valides : {len(objpoints)}")

if len(objpoints) < 6:
    raise RuntimeError(
        "Pas assez d'images valides. "
        "Utilise au moins 6 vues variees, idealement 15 a 25."
    )

# -----------------------------
# Calibration fisheye
# -----------------------------


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
        print(f"Vue {i}: erreur = {error:.3f} pixels")

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
