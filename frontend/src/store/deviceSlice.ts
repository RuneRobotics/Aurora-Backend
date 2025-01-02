import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Camera } from "../types/inputs.ts";
import { Device } from "../types/state_types.ts";

const initialState: Device = {
  ip: "fake ip",
  cameras: [],
};

const DeviceSlice = createSlice({
  name: "device_slice",
  initialState,
  reducers: {
    setIP: (state, action: PayloadAction<string>) => {
      state.ip = action.payload;
    },
    setCameras: (state, action: PayloadAction<Camera[]>) => {
      state.cameras = action.payload;
    },
  },
});

export const { setCameras, setIP } = DeviceSlice.actions;
export default DeviceSlice.reducer;
