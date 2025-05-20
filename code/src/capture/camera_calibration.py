import cv2
import numpy as np
import os

# === Configuration ===
CHESSBOARD_SIZE = (7, 7)
SQUARE_SIZE = 0.28/8
NUM_IMAGES = 20
SAVE_IMAGES = False
SAVE_DIR = "calib_images"
CAMERA_ID = 0

# === Prepare object points ===
objp = np.zeros((CHESSBOARD_SIZE[0] * CHESSBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE

objpoints = []
imgpoints = []

cap = cv2.VideoCapture(CAMERA_ID)
collected = 0

if SAVE_IMAGES and not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

print("Press SPACE to capture a frame if chessboard is detected. Press ESC to quit.")

while collected < NUM_IMAGES:
    ret, frame = cap.read()
    if not ret:
        break

    display_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)

    if found:
        cv2.drawChessboardCorners(display_frame, CHESSBOARD_SIZE, corners, found)

    cv2.imshow("Calibration Feedback", display_frame)
    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break
    elif key == 32 and found:  # SPACE
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        objpoints.append(objp)
        imgpoints.append(corners2)
        collected += 1
        print(f"Captured image {collected}/{NUM_IMAGES}")

        if SAVE_IMAGES:
            cv2.imwrite(f"{SAVE_DIR}/img_{collected}.png", frame)

cap.release()
cv2.destroyAllWindows()

# === Calibration ===
ret, matrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("\n=== Calibration Results ===")
print("Camera Matrix:\n", matrix)
print("Distortion Coefficients:\n", dist)

np.savez("camera_calibration.npz", matrix=matrix, dist=dist)