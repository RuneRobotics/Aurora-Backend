import cv2
import numpy as np
import os

def run_directory_calibration(image_dir, chessboard_size=(7, 7), square_size=0.035):  # adjust square_size if needed
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints = []

    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".png")]

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        if ret:
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1),
                criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            )
            objpoints.append(objp)
            imgpoints.append(corners2)

    if not objpoints:
        raise ValueError("No valid calibration images found.")

    ret, matrix, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )
    if not ret:
        raise ValueError("Calibration failed")

    np.savez(os.path.join(image_dir, "calibration_images.npz"), matrix=matrix, dist=dist)

    return {
        "matrix": matrix.tolist(),
        "distortion": dist.tolist(),
        "num_images": len(objpoints)
    }
