import { Cameras } from "./slices/CameraSlice";
import { Data } from "./slices/DataSlice";
import { LayoutState } from "./slices/LayoutSlice";

export interface State {
  layout: LayoutState;
  cameras: Cameras;
  data: Data;
}
