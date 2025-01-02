import { Alliance, UNKNOWN_TYPE } from "./Constants";

export interface Pose3D {
  pitch: number;
  roll: number;
  x: number;
  y: number;
  yaw: number;
  z: number;
}
export type SafePose3d = UNKNOWN_TYPE | Pose3D;
export interface AprilTag {
  id: number;
  distance: number;
}
export interface targets {
  april_tags: AprilTag[];
}
export interface FusedData {
  robot_position: SafePose3d;
  targets: targets;
}
export interface Camera {
  camera_id: number;
  camera_position: SafePose3d;
  targets: targets;
}
export interface Input {
  fused_data: FusedData;
  cameras: Camera[];
}
export interface Robot {
  position: Pose3D;
  team: number;
  alliance: Alliance;
}
