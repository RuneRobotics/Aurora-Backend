import { configureStore } from "@reduxjs/toolkit";
import deviceReducer from "./deviceSlice";
import dataReducer from "./dataSlice";

export const store = configureStore({
  reducer: {
    devices: deviceReducer,
    data: dataReducer,
  },
});

export type StoreState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
