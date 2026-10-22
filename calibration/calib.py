
import cv2
import numpy as np
import glob
import os
import traceback

# ---------------------------------
# CONFIGURATION
# ---------------------------------

CHECKERBOARD = (6, 8)  # Coins INTERIEURS : colonnes, lignes
SQUARE_SIZE = 80.0    # Taille d'une case en mm

IMAGE_FOLDER = (
    r"C:\Users\raian\Documents\GitHub"
    r"\Var-Drone-soccer\calibration"
)

# ---------------------------------
# RECHERCHE DES IMAGES
# ---------------------------------

print("=== DEBUT DE LA CALIBRATION ===", flush=True)
print("Dossier :", IMAGE_FOLDER, flush=True)

if not os.path.isdir(IMAGE_FOLDER):
    raise FileNotFoundError(f"Dossier introuvable : {IMAGE_FOLDER}")

images = []
for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp"):
    images.extend(glob.glob(os.path.join(IMAGE_FOLDER, ext)))

images = sorted(set(images))

print(f"Images trouvees : {len(images)}", flush=True)

if not images:
    raise RuntimeError("Aucune image trouvee dans le dossier.")

# ---------------------------------
# PREPARATION DES POINTS 3D
# ---------------------------------

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

# ---------------------------------
# DETECTION DU DAMIER
# ---------------------------------

for index, fname in enumerate(images, start=1):
    print(f"\n[{index}/{len(images)}] Lecture : {os.path.basename(fname)}",
          flush=True)

    img = cv2.imread(fname)

    if img is None:
        print("  ERREUR : image illisible.", flush=True)
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if image_size is None:
        image_size = gray.shape[::-1]
        print("  Resolution :", image_size, flush=True)

    if gray.shape[::-1] != image_size:
        print("  Image ignoree : resolution differente.", flush=True)
        continue

    found, corners = cv2.findChessboardCornersSB(
        gray,
        CHECKERBOARD
    )

    if not found or corners is None:
        print(
            f"  DAMI​ER NON DETECTE : verifie CHECKERBOARD={CHECKERBOARD}",
            flush=True
        )
        continue

    corners = cv2.cornerSubPix(
        gray,
        corners,
        (5, 5),
        (-1, -1),
        criteria
    )

    if len(corners) != CHECKERBOARD[0] * CHECKERBOARD[1]:
        print("  ERREUR : nombre de coins incorrect.", flush=True)
        continue

    if not np.isfinite(corners).all():
        print("  ERREUR : coordonnees invalides.", flush=True)
        continue

    imgpoints.append(
        corners.reshape(1, -1, 2).astype(np.float64)
    )
    objpoints.append(objp.copy())

    print(f"  OK : {len(corners)} coins detectes.", flush=True)

    display = img.copy()
    cv2.drawChessboardCorners(display, CHECKERBOARD, corners, True)
    cv2.imshow("Detection du damier - Q pour fermer", display)

    # Appuyer sur Q pour fermer l'affichage des detections
    if cv2.waitKey(200) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break

cv2.destroyAllWindows()

print("\n=== BILAN DE LA DETECTION ===", flush=True)
print(f"Images examinees : {len(images)}", flush=True)
print(f"Images valides   : {len(objpoints)}", flush=True)

if len(objpoints) < 8:
    raise RuntimeError(
        f"Seulement {len(objpoints)} images valides. "
        "Il en faut au moins 8 pour tenter cette calibration."
    )

# ---------------------------------
# CALIBRATION FISHEYE
# ---------------------------------

print("\n=== LANCEMENT DE LA CALIBRATION FISHEYE ===", flush=True)

height = image_size[1]
width = image_size[0]

# Estimation initiale des paramètres de la caméra
f = min(width, height) * 0.5

K = np.array([
    [f, 0.0, width / 2.0],
    [0.0, f, height / 2.0],
    [0.0, 0.0, 1.0]
], dtype=np.float64)

D = np.zeros((4, 1), dtype=np.float64)

# Utiliser l'estimation initiale et fixer le skew à zéro.
# On retire RECOMPUTE_EXTRINSIC pour ce premier essai.
flags = (
    cv2.fisheye.CALIB_USE_INTRINSIC_GUESS
    | cv2.fisheye.CALIB_FIX_SKEW
)

print("Resolution :", width, "x", height, flush=True)
print("Focale initiale :", f, flush=True)
print("Matrice K initiale :\n", K, flush=True)
print("Lancement de cv2.fisheye.calibrate...", flush=True)
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
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            200,
            1e-7
        )
    )

except Exception:
    print("\n!!! ECHEC DE LA CALIBRATION !!!", flush=True)
    traceback.print_exc()
    raise

# ---------------------------------
# CALCUL DES ERREURS
# ---------------------------------

print("\n=== ERREURS DE REPROJECTION ===", flush=True)

errors = []

for i in range(len(objpoints)):
    try:
        projected, _ = cv2.fisheye.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], K, D
        )

        observed = imgpoints[i].reshape(-1, 2)
        projected = projected.reshape(-1, 2)

        error = np.sqrt(
            np.mean(np.sum((observed - projected) ** 2, axis=1))
        )

        errors.append(error)
        print(f"Vue {i + 1}: {error:.3f} pixels", flush=True)

    except Exception:
        print(f"Erreur lors du calcul pour la vue {i + 1} :", flush=True)
        traceback.print_exc()

if errors:
    print(f"\nRMS OpenCV           : {rms:.4f}", flush=True)
    print(f"Erreur moyenne       : {np.mean(errors):.3f} pixels", flush=True)
    print(f"Erreur maximale      : {np.max(errors):.3f} pixels", flush=True)

if not np.isfinite(K).all() or not np.isfinite(D).all():
    raise RuntimeError("Les parametres de calibration sont invalides.")

# ---------------------------------
# SAUVEGARDE
# ---------------------------------

output_path = os.path.join(IMAGE_FOLDER, "calib.yml")

fs = cv2.FileStorage(output_path, cv2.FILE_STORAGE_WRITE)

if not fs.isOpened():
    raise RuntimeError(f"Impossible de creer le fichier : {output_path}")

fs.write("K", K)
fs.write("D", D)
fs.write("image_width", image_size[0])
fs.write("image_height", image_size[1])
fs.release()

print("\n=== CALIBRATION TERMINEE ===", flush=True)
print("Fichier sauvegarde :", output_path, flush=True)
print("Matrice K :\n", K, flush=True)
print("Coefficients D :\n", D, flush=True)
