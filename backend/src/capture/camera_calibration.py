import cv2
import numpy as np
import os

def calibrate_camera(image_folder, chessboard_size=(9, 6), square_size=1.0):
    """
    Calibrate a camera using images of a chessboard.

    Args:
        image_folder (str): Path to the folder containing chessboard images.
        chessboard_size (tuple): Number of inner corners per chessboard row and column (rows, columns).
        square_size (float): Size of a square on the chessboard in your desired units (e.g., meters, centimeters).

    Returns:
        ret (float): Overall RMS re-projection error.
        camera_matrix (numpy.ndarray): Camera matrix.
        dist_coeffs (numpy.ndarray): Distortion coefficients.
        rvecs (list): Rotation vectors for each image.
        tvecs (list): Translation vectors for each image.
    """
    # Termination criteria for corner subpixel accuracy
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points (3D points in real-world space)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size

    # Arrays to store object points and image points from all the images
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in image plane

    # Iterate through images in the folder
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in images:
        img_path = os.path.join(image_folder, image_file)
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)

            # Refine corner locations
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners (optional, for debugging)
            cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
            cv2.imshow('Chessboard', img)
            cv2.waitKey(100)

    cv2.destroyAllWindows()

    # Calibrate the camera
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    return ret, camera_matrix, dist_coeffs, rvecs, tvecs