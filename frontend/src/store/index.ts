import { configureStore } from "@reduxjs/toolkit";
import fusedDataReducer from "./FusedDataSlice";
import deviceReducer from "./CoProcessorSlice";
import layoutReducer from "./LayoutSlice";
export const store = configureStore({
  reducer: {
    fused_data_slice: fusedDataReducer,
    device_slice: deviceReducer,
    layout_slice: layoutReducer,
  },
});

export type StoreState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
