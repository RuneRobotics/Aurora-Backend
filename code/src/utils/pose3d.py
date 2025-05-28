import numpy as np

class Pose3D:
    """
    Represents a 3D pose with position and orientation.

    Attributes:
        x (float): X-coordinate of the pose.
        y (float): Y-coordinate of the pose.
        z (float): Z-coordinate of the pose.
        roll (float): Rotation around the X-axis in radians.
        pitch (float): Rotation around the Y-axis in radians.
        yaw (float): Rotation around the Z-axis in radians.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, roll: float = 0.0, pitch: float = 0.0, yaw: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def equals(self, other: object) -> bool:
        """
        Checks if two Pose3D objects are equal.

        Two Pose3D objects are considered equal if their position (x, y, z)
        and orientation (roll, pitch, yaw) values are numerically close within
        a small tolerance.

        Args:
            other (Pose3D): The other Pose3D instance to compare.

        Returns:
            bool: True if the poses are approximately equal, False otherwise.
        """
        if not isinstance(other, Pose3D):
            return False
        return np.allclose(
            [self.x, self.y, self.z, self.roll, self.pitch, self.yaw],
            [other.x, other.y, other.z, other.roll, other.pitch, other.yaw]
        )
    
    def to_string(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}, roll: {self.roll}, pitch: {self.pitch}, yaw: {self.yaw}"