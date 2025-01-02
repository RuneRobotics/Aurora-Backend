import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { AprilTag, FusedData, SafePose3d } from "../types/inputs.ts";
import { UNKNOWN } from "../types/Constants.ts";

const initialState: FusedData = {
  robot_position: UNKNOWN,
  targets: {
    april_tags: [],
  },
};

const FusedDataSlice = createSlice({
  name: "fused_data_slice",
  initialState,
  reducers: {
    setRobotPosition: (state, action: PayloadAction<SafePose3d>) => {
      state.robot_position = action.payload;
    },
    setTags: (state, action: PayloadAction<AprilTag[]>) => {
      state.targets.april_tags = action.payload;
    },
  },
});

export const { setRobotPosition, setTags } = FusedDataSlice.actions;
export default FusedDataSlice.reducer;
