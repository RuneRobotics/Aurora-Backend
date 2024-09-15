import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface Device {
  IP: string;
  cameraAmount: number;
}
export interface selectedCamera {
  selectedCameraDeviceIP: string;
  selectedCameraIndex: number;
}
export interface Cameras {
  devices: Device[];
  selection?: selectedCamera;
}
const initialState: Cameras = {
  devices: [
    { IP: "0", cameraAmount: 1 },
    { IP: "0", cameraAmount: 1 },
    { IP: "2", cameraAmount: 3 },
    { IP: "3", cameraAmount: 1 },
    { IP: "4", cameraAmount: 1 },
  ],
  selection: {
    selectedCameraDeviceIP: "0.0.0.0",
    selectedCameraIndex: 0,
  },
};
const camerasSlice = createSlice({
  name: "cameras",
  initialState,
  reducers: {
    setSelection: (state, action: PayloadAction<selectedCamera>) => {
      const device = state.devices.filter(
        (device) => device.IP === action.payload.selectedCameraDeviceIP
      );
      if (
        device.length >= 1 &&
        device[0].cameraAmount >= action.payload.selectedCameraIndex
      ) {
        state.selection = action.payload;
      }
    },
  },
});

export const { setSelection } = camerasSlice.actions;
export default camerasSlice.reducer;
