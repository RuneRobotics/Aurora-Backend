import cv2
import numpy as np
import apriltag

class AprilTagDetector:
    def __init__(self):
        # Initialize the AprilTag detector
        self.detector = apriltag.Detector()

    def detect_tags(self, image):
        # Convert the image to grayscale for tag detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect AprilTags
        tags = self.detector.detect(gray)

        tag_positions = []
        tag_ids = []

        for tag in tags:
            # Each tag contains 2D image coordinates (corners of the tag)
            tag_positions.append(tag.corners)
            # Append the tag ID
            tag_ids.append(tag.tag_id)

            # Draw the detected tags on the image
            for idx, corner in enumerate(tag.corners):
                corner = (int(corner[0]), int(corner[1]))
                cv2.circle(image, corner, 5, (0, 255, 0), -1)
            
            # Add tag ID as text on the image
            cv2.putText(image, f"ID: {tag.tag_id}", (int(tag.corners[0][0]), int(tag.corners[0][1] - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return image, tag_positions, tag_ids

# Test script
if __name__ == "__main__":
    tag_detector = AprilTagDetector()
    image = cv2.imread('data/test_images/test_apriltag.jpg')

    # Detect the AprilTags
    result_image, tag_positions, tag_ids = tag_detector.detect_tags(image)

    # Show the result image with detected tags
    cv2.imshow('AprilTag Detection', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Print the detected tag positions and IDs
    print("Detected Tags:")
    for pos, tag_id in zip(tag_positions, tag_ids):
        print(f"Tag ID: {tag_id}, Position: {pos}")
