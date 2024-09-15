import { createSlice } from "@reduxjs/toolkit";
import { selectedCamera } from "./CameraSlice";
interface WatchingCamera {
  camera: selectedCamera;
  certainty: number;
}
export interface note {
  x: number;
  y: number;
  cameras: WatchingCamera[];
}
enum Color {
  RED,
  BLUE,
}
export interface Robot {
  x: number;
  y: number;
  rotation: number;
  width: number;
  length: number;
  color: Color;
  team: number;
  cameras: WatchingCamera[];
}
export interface AprilTag {
  id: number;
  x: number;
  y: number;
  z: number;
  roll: number;
  pitch: number;
  yaw: number;
  cameras: WatchingCamera[];
}
interface position {
  length: number;
  width: number;
  x: number;
  y: number;
  z: number;
  roll: number;
  pitch: number;
  yaw: number;
  cameras: WatchingCamera[];
}
export interface Data {
  notes: note[];
  robots: Robot[];
  aprilTags: AprilTag[];
  pose: position;
}
const initialState: Data = {
  notes: [],
  robots: [],
  aprilTags: [],
  pose: {
    x: 0,
    y: 0,
    z: 0,
    roll: 0,
    pitch: 0,
    yaw: 0,
    cameras: [],
    width: 0.73,
    length: 0.73,
  },
};

const dataSlice = createSlice({
  name: "data",
  initialState,
  reducers: {},
});

export const {} = dataSlice.actions;
export default dataSlice.reducer;
