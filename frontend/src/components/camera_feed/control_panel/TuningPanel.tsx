import { Box, Slider, Typography } from "@mui/material";
import { StoreState } from "../../../store";
import { useDispatch, useSelector } from "react-redux";
import { LightingState } from "../../../types/state_types";
import { setLighting } from "../../../store/LayoutSlice";

const TuningPanel: React.FC = () => {
  const dispatch = useDispatch();
  const mode = useSelector(
    (state: StoreState) => state.layout_slice.selectedCamera?.mode
  );
  const state = useSelector(
    (state: StoreState) => state.layout_slice.selectedCamera?.cameraState
  );
  const handleLightingChange = (key: "brightness" | "exposure") => {
    return (_event: Event, value: number | number[]) => {
      if (typeof value !== "number") {
        return;
      }
      dispatch(setLighting({ value: value, key }));
    };
  };
  if (mode === "Lighting") {
    const lightingState = state as LightingState;
    return (
      <Box sx={{ flex: 1 }}>
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom color="text.secondary">
            Exposure ({lightingState.exposure}%)
          </Typography>
          <Slider
            value={lightingState.exposure}
            onChange={handleLightingChange("exposure")}
            min={0}
            max={100}
            valueLabelDisplay="auto"
          />
        </Box>
        <Box>
          <Typography gutterBottom color="text.secondary">
            Brightness ({lightingState.brightness}%)
          </Typography>
          <Slider
            value={lightingState.brightness}
            onChange={handleLightingChange("brightness")}
            min={0}
            max={100}
            valueLabelDisplay="auto"
          />
        </Box>
      </Box>
    );
  }
  return <></>;
};
export default TuningPanel;
