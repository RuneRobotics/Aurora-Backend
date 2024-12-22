import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface DeviceState {
  selectedCamera: string | null;
  isCanvasView: boolean;
  calibrationImages: Record<string, string[]>;
  currentImageIndex: Record<string, number>;
  tuningSettings: Record<string, { exposure: number; brightness: number }>;
}

const initialState: DeviceState = {
  selectedCamera: null,
  isCanvasView: false,
  calibrationImages: {},
  currentImageIndex: {},
  tuningSettings: {},
};

const deviceSlice = createSlice({
  name: "devices",
  initialState,
  reducers: {
    setSelectedCamera: (state, action: PayloadAction<string | null>) => {
      state.selectedCamera = action.payload;
      if (action.payload && !state.tuningSettings[action.payload]) {
        state.tuningSettings[action.payload] = { exposure: 50, brightness: 50 };
      }
    },
    toggleView: (state) => {
      state.isCanvasView = !state.isCanvasView;
    },
    addCalibrationImage: (
      state,
      action: PayloadAction<{ cameraId: string; imageData: string }>
    ) => {
      const { cameraId, imageData } = action.payload;
      if (!state.calibrationImages[cameraId]) {
        state.calibrationImages[cameraId] = [];
        state.currentImageIndex[cameraId] = 0;
      }
      state.calibrationImages[cameraId].push(imageData);
      state.currentImageIndex[cameraId] =
        state.calibrationImages[cameraId].length - 1;
    },
    deleteLastCalibrationImage: (state, action: PayloadAction<string>) => {
      const cameraId = action.payload;
      if (state.calibrationImages[cameraId]?.length > 0) {
        state.calibrationImages[cameraId].splice(
          state.currentImageIndex[cameraId],
          1
        );
        if (
          state.currentImageIndex[cameraId] >=
          state.calibrationImages[cameraId].length
        ) {
          state.currentImageIndex[cameraId] = Math.max(
            0,
            state.calibrationImages[cameraId].length - 1
          );
        }
      }
    },
    clearCalibrationImages: (state, action: PayloadAction<string>) => {
      const cameraId = action.payload;
      state.calibrationImages[cameraId] = [];
      state.currentImageIndex[cameraId] = 0;
    },
    updateTuningSettings: (
      state,
      action: PayloadAction<{
        cameraId: string;
        setting: "exposure" | "brightness";
        value: number;
      }>
    ) => {
      const { cameraId, setting, value } = action.payload;
      if (!state.tuningSettings[cameraId]) {
        state.tuningSettings[cameraId] = { exposure: 50, brightness: 50 };
      }
      state.tuningSettings[cameraId][setting] = value;
    },
    navigateCalibrationImage: (
      state,
      action: PayloadAction<{
        cameraId: string;
        direction: "prev" | "next";
      }>
    ) => {
      const { cameraId, direction } = action.payload;
      if (!state.calibrationImages[cameraId]?.length) return;

      if (direction === "next") {
        state.currentImageIndex[cameraId] =
          (state.currentImageIndex[cameraId] + 1) %
          state.calibrationImages[cameraId].length;
      } else {
        state.currentImageIndex[cameraId] =
          state.currentImageIndex[cameraId] === 0
            ? state.calibrationImages[cameraId].length - 1
            : state.currentImageIndex[cameraId] - 1;
      }
    },
  },
});

export const {
  setSelectedCamera,
  toggleView,
  addCalibrationImage,
  deleteLastCalibrationImage,
  clearCalibrationImages,
  updateTuningSettings,
  navigateCalibrationImage,
} = deviceSlice.actions;

export default deviceSlice.reducer;
