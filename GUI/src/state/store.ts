// src/redux/store.ts
import { configureStore } from "@reduxjs/toolkit";
import layoutReducer from "./slices/LayoutSlice";
import camerReducer from "./slices/CameraSlice";

export const store = configureStore({
  reducer: {
    layout: layoutReducer,
    cameras: camerReducer,
  },
});

// Type definitions for store
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
