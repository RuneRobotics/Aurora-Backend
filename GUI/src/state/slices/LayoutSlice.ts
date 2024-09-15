import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export enum LayoutType {
  FIELD,
  CAM,
  BOTH,
}
export enum ScreenSide {
  LEFT = 1,
  RIGHT = -1,
}
export interface LayoutState {
  layoutType: LayoutType;
  sideCams: boolean;
  screenSide: ScreenSide;
}

const initialState: LayoutState = {
  layoutType: LayoutType.BOTH,
  sideCams: true,
  screenSide: ScreenSide.LEFT,
};

const layoutSlice = createSlice({
  name: "layout",
  initialState,
  reducers: {
    toggleSide: (state) => {
      state.screenSide =
        state.screenSide === ScreenSide.LEFT
          ? ScreenSide.RIGHT
          : ScreenSide.LEFT;
    },
    toggleSideCams: (state) => {
      state.sideCams = !state.sideCams;
    },
    setLayoutType: (state, action: PayloadAction<LayoutType>) => {
      state.layoutType = action.payload;
    },
  },
});

export const { toggleSide, toggleSideCams, setLayoutType } =
  layoutSlice.actions;
export default layoutSlice.reducer;
