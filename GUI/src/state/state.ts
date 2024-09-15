import { Cameras } from "./slices/CameraSlice";
import { LayoutState } from "./slices/LayoutSlice";

export interface State {
  layout: LayoutState;
  cameras: Cameras;
}
