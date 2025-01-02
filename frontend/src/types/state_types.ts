import { PNG, TargetType } from "./Constants";
import { Camera } from "./inputs";

export interface Device {
  ip: string;
  cameras: Camera[];
}
export const enum View {
  Field = "Field",
  Camera = "Camera",
}
export enum Mode {
  Calibration = "Calibration",
  Detection = "Detection",
  Lighting = "Lighting",
}
export interface CalibrationState {
  imageCount: number;
  currentIndex: number | undefined;
  calibrationImages: PNG[];
}
export interface DetectionState {
  targetType: TargetType;
}
export interface LightingState {
  brightness: number;
  exposure: number;
}

export interface CameraState {
  id: number;
  mode: Mode;
  cameraState: CalibrationState | DetectionState | LightingState;
}
export interface Layout {
  selectedCamera: CameraState | undefined;
  view: View;
}
