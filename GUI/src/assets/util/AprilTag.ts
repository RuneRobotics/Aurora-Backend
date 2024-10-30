import { tags } from "./AprilTagLayout.json";
interface Quaternion {
  W: number;
  X: number;
  Y: number;
  Z: number;
}

interface Translation {
  x: number;
  y: number;
  z: number;
}

interface Pose {
  translation: Translation;
  rotation: {
    quaternion: Quaternion;
  };
}

interface Tag {
  ID: number;
  pose: Pose;
}

interface Data {
  tags: Tag[];
}

const data: Data = { tags: tags };

export function getTagPose(
  id: number
): { x: number; y: number; rotation: number } | null {
  const tag = data.tags.find((tag) => tag.ID === id);
  if (!tag) return null;

  const { x, y } = tag.pose.translation;
  const { quaternion } = tag.pose.rotation;

  // Calculate yaw from quaternion
  const rotation = 2 * Math.acos(quaternion.W);

  return { x, y, rotation };
}
