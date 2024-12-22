export interface Camera {
  id: string;
  name: string;
  feed: string;
  data: Record<string, any>;
}

export interface Device {
  id: string;
  name: string;
  ipAddress: string;
  cameras: Camera[];
}

export interface RootState {
  devices: {
    items: Device[];
    selectedCamera: string | null;
    isCanvasView: boolean;
    calibrationImages: Record<string, string[]>;
    currentImageIndex: Record<string, number>;
    tuningSettings: Record<string, { exposure: number; brightness: number }>;
  };
}
export interface Data {
  devices: DeviceData[];
  fused_data: FusedData;
}
export interface FusedData {
  targets: targets;
  position: Pose2d & { certainty: number };
}
interface targets {
  notes: Note[];
  apriltags: AprilTag[];
  robots: Robot[];
}
export interface DeviceData {
  id: string;
  name: string;
  ipAddress: string;
  cameras: CameraData[];
}
export interface CameraData {
  notes: Note[];
  apriltags: AprilTag[];
  robots: Robot[];
  position: Pose3d;
}
export interface Note {
  certainty: number;
  position: Translation2d;
}
export interface AprilTag {
  id: number;
  certainty: number;
  position: Pose3d; //camera relative
}
export interface Robot {
  team: number;
  alliance: Alliance;
  position: Pose2d;
  certainty: number;
}
export interface Translation2d {
  x: number;
  y: number;
}
export interface Pose2d {
  x: number;
  y: number;
  yaw: number;
}
export interface Pose3d {
  x: number;
  y: number;
  z: number;
  roll: number;
  pitch: number;
  yaw: number;
}
export type Alliance = "BLUE" | "RED";
export const modes = ["data", "tuning", "calibration"] as const;
export type Mode = "data" | "tuning" | "calibration";
export const targets = ["apriltags", "robots", "notes"] as const;
export type TargetType = "apriltags" | "robots" | "notes";
export type LightingSettings = {
  exposure: number;
  brightness: number;
} | null;
