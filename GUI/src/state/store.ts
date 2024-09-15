// src/redux/store.ts
import { configureStore } from "@reduxjs/toolkit";
import layoutReducer from "./slices/LayoutSlice";
import camerasReducer from "./slices/CameraSlice";
import dataReducer from "./slices/DataSlice";

export const store = configureStore({
  reducer: {
    layout: layoutReducer,
    cameras: camerasReducer,
    data: dataReducer,
  },
});

// Type definitions for store
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
