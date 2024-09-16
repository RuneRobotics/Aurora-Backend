import { createSlice } from "@reduxjs/toolkit";
import { selectedCamera } from "./CameraSlice";
interface WatchingCamera {
  camera: selectedCamera;
  certainty: number;
}
export interface Note {
  x: number;
  y: number;
  cameras: WatchingCamera[];
}
export enum Color {
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
export interface position {
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
  notes: Note[];
  robots: Robot[];
  aprilTags: AprilTag[];
  pose: position;
}
const initialState: Data = {
  notes: [
    {
      x: 1,
      y: 2,
      cameras: [],
    },
    {
      x: 3,
      y: 4,
      cameras: [],
    },
    {
      x: 5,
      y: 6,
      cameras: [],
    },
    {
      x: 4,
      y: 3,
      cameras: [],
    },
  ],
  robots: [
    {
      x: 1,
      y: 1,
      rotation: 0,
      width: 0.7,
      length: 0.8,
      color: Color.RED,
      team: 0,
      cameras: [],
    },
    {
      x: 2,
      y: 2,
      rotation: 0,
      width: 1,
      length: 0.5,
      color: Color.BLUE,
      team: 5990,
      cameras: [],
    },
    {
      x: 4,
      y: 4,
      rotation: 0,
      width: 0.8,
      length: 0.8,
      color: Color.RED,
      team: 0,
      cameras: [],
    },
  ],
  aprilTags: [
    {
      id: 0,
      x: 4,
      y: 4,
      z: 0,
      roll: 0,
      pitch: 0,
      yaw: 2,
      cameras: [],
    },
    {
      id: 0,
      x: 3,
      y: 3,
      z: 0,
      roll: 0,
      pitch: 0,
      yaw: 2,
      cameras: [],
    },
    {
      id: 0,
      x: 12,
      y: 2,
      z: 0,
      roll: 0,
      pitch: 0,
      yaw: 0,
      cameras: [],
    },
  ],
  pose: {
    x: 10,
    y: 3,
    z: 0,
    roll: 0,
    pitch: 0,
    yaw: 0.4,
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
