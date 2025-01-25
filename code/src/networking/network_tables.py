from ntcore import NetworkTableInstance

from capture.camera import Pose3D
class RobotPosePublisher:
    def __init__(self, team_number: int):
        # Initialize NetworkTables instance
        self.ntinst = NetworkTableInstance.getDefault()
        self.ntinst.startClient4("aurora_client")  # Connect to the FRC team's network
        self.ntinst.setServerTeam(team_number)

        # Get or create the "RobotPose" table
        self.robot_pose_table = self.ntinst.getTable("Aurora/Localization")

    def update_pose(self, pose: Pose3D):
        # Publish values to the "RobotPose" table
        self.robot_pose_table.putNumber("X", pose.x)
        self.robot_pose_table.putNumber("Y", pose.y)
        self.robot_pose_table.putNumber("Z", pose.z)
        self.robot_pose_table.putNumber("Roll", pose.roll)
        self.robot_pose_table.putNumber("Pitch", pose.pitch)
        self.robot_pose_table.putNumber("Yaw", pose.yaw)