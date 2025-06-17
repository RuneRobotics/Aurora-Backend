import cv2
import numpy as np
import os

def calibrate_camera(image_dir, calibration_settings):
    # === Extract settings ===
    rows = calibration_settings["rows"]
    columns = calibration_settings["columns"]
    square_size = calibration_settings["sideLength"] / 1000.0  # convert mm to meters if needed
    image_size = (
        calibration_settings["imageSize"]["width"],
        calibration_settings["imageSize"]["height"]
    )
    chessboard_size = (columns, rows)

    # === Prepare object points ===
    objp = np.zeros((rows * columns, 3), np.float32)
    objp[:, :2] = np.mgrid[0:columns, 0:rows].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints = []

    # === Load images ===
    images = sorted(
        [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".png") or f.endswith(".jpg")]
    )

    print("Press SPACE to use a frame if corners are correctly detected. Press ESC to skip.")

    for fname in images:
        frame = cv2.imread(fname)
        if frame is None:
            print(f"Skipping unreadable image: {fname}")
            continue

        display_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        found, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        if found:
            cv2.drawChessboardCorners(display_frame, chessboard_size, corners, found)

        cv2.imshow("Calibration Image", display_frame)
        key = cv2.waitKey(0)

        if key == 27:  # ESC - skip this image
            continue
        elif key == 32 and found:  # SPACE - use this image
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1),
                criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            )
            objpoints.append(objp)
            imgpoints.append(corners2)
            print(f"Accepted image: {os.path.basename(fname)}")
        else:
            print(f"Skipped image: {os.path.basename(fname)}")

    cv2.destroyAllWindows()

    if not objpoints:
        raise ValueError("No valid calibration data collected.")

    # === Calibration ===
    ret, matrix, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, image_size, None, None
    )

    if not ret:
        raise RuntimeError("Camera calibration failed.")

    # Save calibration result
    np.savez(os.path.join(image_dir, "camera_calibration.npz"), matrix=matrix, dist=dist)

    print("\n=== Calibration Complete ===")
    print("Camera Matrix:\n", matrix)
    print("Distortion Coefficients:\n", dist)

    return {
        "matrix": matrix.tolist(),
        "distortion": dist.tolist(),
        "num_images": len(objpoints)
    }


def delete_image(index):
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calibration_images')
    
    # Get all image filenames in the directory and sort them
    image_files = sorted(
        [f for f in os.listdir(dir_path) if f.startswith("image_") and f.endswith(".png")],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )

    # Check if index is valid
    if index < 0 or index >= len(image_files):
        print(f"Invalid index: {index}")
        return

    # Delete the specified image
    os.remove(os.path.join(dir_path, image_files[index]))

    # Rename remaining images to keep the numbering contiguous
    image_files.pop(index)
    for new_index, filename in enumerate(image_files):
        old_path = os.path.join(dir_path, filename)
        new_path = os.path.join(dir_path, f"image_{new_index}.png")
        os.rename(old_path, new_path)

def save_image(frame):
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calibration_images')
    num_files = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
    image_path = os.path.join(dir_path, f"image_{num_files}.png")
    cv2.imwrite(image_path, frame)

    return num_files