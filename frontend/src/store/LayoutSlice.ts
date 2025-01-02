import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Layout, Mode, View, CalibrationState } from "../types/state_types.ts";
import { PNG, TargetType } from "../types/Constants.ts";

const initialState: Layout = {
  selectedCamera: undefined,
  view: View.Field,
};
const getCameraState = (mode: Mode, _cameraID: number) => {
  switch (mode) {
    case Mode.Calibration:
      return {
        imageCount: 0,
        currentIndex: undefined,
        calibrationImages: [],
      };
    case Mode.Detection:
      return {
        targetType: TargetType.AprilTag,
      };
    case Mode.Lighting:
      return {
        brightness: 0,
        exposure: 0,
      };
  }
};
const LayoutSlice = createSlice({
  name: "layout_slice",
  initialState,
  reducers: {
    setSelectedCameraID: (state, action: PayloadAction<number | undefined>) => {
      console.log("setSelectedCameraID " + action.payload);
      if (action.payload == undefined) {
        state.selectedCamera = undefined;
        state.view = View.Field;
        return;
      }
      state.view = View.Camera;
      state.selectedCamera = {
        id: action.payload,
        mode: Mode.Calibration,
        cameraState: getCameraState(Mode.Calibration, action.payload),
      };
    },
    toggleView: (state) => {
      if (state.view == View.Field) {
        state.view = View.Camera;
        return;
      }
      state.view = View.Field;
      state.selectedCamera = undefined;
    },
    setMode(state, action: PayloadAction<Mode>) {
      if (state.selectedCamera == undefined) {
        return;
      }
      state.selectedCamera = {
        id: state.selectedCamera.id,
        mode: action.payload,
        cameraState: getCameraState(action.payload, state.selectedCamera.id),
      };
    },
    navigateImage(state, action: PayloadAction<"prev" | "next">) {
      if (state.selectedCamera == undefined) {
        return;
      }
      if (state.selectedCamera.mode === Mode.Calibration) return;
      const cameraState = state.selectedCamera.cameraState as CalibrationState;
      if (cameraState.currentIndex === undefined) return;
      if (action.payload === "prev") {
        cameraState.currentIndex =
          (cameraState.currentIndex - 1 + cameraState.imageCount) %
          cameraState.imageCount;
      } else {
        cameraState.currentIndex =
          (cameraState.currentIndex + 1) % cameraState.imageCount;
      }
    },
    setLighting(
      state,
      action: PayloadAction<{ value: number; key: "brightness" | "exposure" }>
    ) {
      if (
        state.selectedCamera &&
        "brightness" in state.selectedCamera.cameraState &&
        "exposure" in state.selectedCamera.cameraState
      ) {
        state.selectedCamera.cameraState[action.payload.key] =
          action.payload.value;
      }
    },
    getSnapshot(state, action: PayloadAction<PNG>) {
      const cameraState = state.selectedCamera?.cameraState;
      if (!cameraState) return;
      if (state.selectedCamera && "calibrationImages" in cameraState) {
        (cameraState as CalibrationState).calibrationImages.push(
          action.payload
        );
        (cameraState as CalibrationState).imageCount++;
        const index = (cameraState as CalibrationState).currentIndex;
        (cameraState as CalibrationState).currentIndex = index ? index + 1 : 0;
      }
    },
    deleteSnapshot(state) {
      const cameraState = state.selectedCamera?.cameraState;
      if (!cameraState) return;
      if (state.selectedCamera && "calibrationImages" in cameraState) {
        const index = (cameraState as CalibrationState).currentIndex;
        if (index === undefined) return;
        (cameraState as CalibrationState).calibrationImages.splice(index, 1);
        (cameraState as CalibrationState).imageCount--;
        const imageCount = (cameraState as CalibrationState).imageCount;
        (cameraState as CalibrationState).currentIndex =
          (index - 1 + imageCount) % imageCount;
      }
    },
  },
});

export const {
  setSelectedCameraID,
  toggleView,
  setMode,
  setLighting,
  navigateImage,
  getSnapshot,
  deleteSnapshot,
} = LayoutSlice.actions;
export default LayoutSlice.reducer;
