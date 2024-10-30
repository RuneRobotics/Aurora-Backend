import { createSlice, PayloadAction } from "@reduxjs/toolkit";
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
  /*x: number;
  y: number;
  z: number;
  roll: number;
  pitch: number;
  yaw: number;*/
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
  notes: [],
  robots: [],
  aprilTags: [],
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
  reducers: {
    setPosition: (state, action: PayloadAction<position>) => {
      state.pose = action.payload;
    },
    setTags: (state, action: PayloadAction<AprilTag[]>) => {
      state.aprilTags = action.payload;
    },
  },
});

export const { setPosition, setTags } = dataSlice.actions;
export default dataSlice.reducer;
