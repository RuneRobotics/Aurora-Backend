from pathlib import Path
import numpy as np
import cv2

def calibrate_camera(image_folder: Path, chessboard_size: tuple[int, int] = (9, 6), square_size: float = 1.0) -> tuple[float, np.ndarray, np.ndarray]:
    """
    Calibrate a camera using images of a chessboard.

    Args:
        image_folder (Path): Path to the folder containing chessboard images.
        chessboard_size (tuple[int, int]): Number of inner corners per chessboard row and column (rows, columns).
        square_size (float): Size of a square on the chessboard in your desired units (e.g., meters, centimeters).

    Returns:
        tuple[float, np.ndarray, np.ndarray, list[np.ndarray], list[np.ndarray]]:
            - ret (float): Overall RMS re-projection error.
            - camera_matrix (numpy.ndarray): Camera matrix.
            - dist_coeffs (numpy.ndarray): Distortion coefficients.
    """
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints = []

    images = list(image_folder.glob("*.png")) + list(image_folder.glob("*.jpg")) + list(image_folder.glob("*.jpeg"))

    for img_path in images:
        img = cv2.imread(str(img_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    return ret, camera_matrix, dist_coeffs
