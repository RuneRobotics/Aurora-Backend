import { CameraData, Pose2d, Pose3d, Translation2d } from "../types";

export const formatPose2d = (pose: Pose2d): Record<string, string> => ({
  "X Position": `${pose.x.toFixed(2)}m`,
  "Y Position": `${pose.y.toFixed(2)}m`,
  Yaw: `${pose.yaw.toFixed(2)}°`,
});

export const formatPose3d = (pose: Pose3d): Record<string, string> => ({
  "X Position": `${pose.x.toFixed(2)}m`,
  "Y Position": `${pose.y.toFixed(2)}m`,
  "Z Position": `${pose.z.toFixed(2)}m`,
  Roll: `${pose.roll.toFixed(2)}°`,
  Pitch: `${pose.pitch.toFixed(2)}°`,
  Yaw: `${pose.yaw.toFixed(2)}°`,
});

export const formatTranslation2d = (
  translation: Translation2d
): Record<string, string> => ({
  "X Position": `${translation.x.toFixed(2)}m`,
  "Y Position": `${translation.y.toFixed(2)}m`,
});

export const formatCameraData = (data: CameraData): Record<string, string> => {
  const formattedData: Record<string, string> = {
    "Notes Detected": data.notes.length.toString(),
    "AprilTags Detected": data.apriltags.length.toString(),
    "Robots Detected": data.robots.length.toString(),
    ...formatPose3d(data.position),
  };

  // Add note positions if any
  data.notes.forEach((note, index) => {
    formattedData[`Note ${index + 1} Position`] = `(${note.position.x.toFixed(
      2
    )}m, ${note.position.y.toFixed(2)}m)`;
    formattedData[`Note ${index + 1} Certainty`] = `${(
      note.certainty * 100
    ).toFixed(1)}%`;
  });

  // Add apriltag data if any
  data.apriltags.forEach((tag, index) => {
    formattedData[`AprilTag ${index + 1} ID`] = tag.id.toString();
    formattedData[`AprilTag ${index + 1} Certainty`] = `${(
      tag.certainty * 100
    ).toFixed(1)}%`;
    if (tag.position) {
      formattedData[
        `AprilTag ${index + 1} Position`
      ] = `(${tag.position.x.toFixed(2)}m, ${tag.position.y.toFixed(
        2
      )}m, ${tag.position.z.toFixed(2)}m)`;
    }
  });

  // Add robot data if any
  data.robots.forEach((robot, index) => {
    formattedData[`Robot ${index + 1} Team`] = robot.team.toString();
    formattedData[`Robot ${index + 1} Alliance`] = robot.alliance;
    formattedData[`Robot ${index + 1} Position`] = `(${robot.position.x.toFixed(
      2
    )}m, ${robot.position.y.toFixed(2)}m, ${robot.position.z.toFixed(2)}m)`;
  });

  return formattedData;
};
