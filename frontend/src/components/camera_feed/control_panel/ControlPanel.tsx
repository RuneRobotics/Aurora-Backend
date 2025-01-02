import { Box, MenuItem, Paper, TextField, Typography } from "@mui/material";
import TuningPanel from "./TuningPanel";
import CalibrationPanel from "./CalibrationPanel";
import DataPanel from "./DataPanel";
import { MIN_CONTROL_CARD_WIDTH } from "../../../types/Constants";
import { StoreState } from "../../../store";
import { useDispatch, useSelector } from "react-redux";
import { setMode } from "../../../store/LayoutSlice";
import { Mode } from "../../../types/state_types";

interface Props {
  isSmallScreen: boolean;
}
const PanelFromMode: React.FC<{ mode: Mode }> = ({ mode }: { mode: Mode }) => {
  switch (mode) {
    case Mode.Calibration:
      return <CalibrationPanel />;
    case Mode.Lighting:
      return <TuningPanel />;
  }
  return <DataPanel />;
};
const ControlPanel: React.FC<Props> = ({ isSmallScreen }: Props) => {
  const dispatch = useDispatch();
  const selectedCamera = useSelector(
    (state: StoreState) => state.layout_slice.selectedCamera
  );
  const mode = useSelector(
    (state: StoreState) => state.layout_slice.selectedCamera?.mode
  );
  if (!selectedCamera || !mode) return <></>;

  return (
    <Paper
      elevation={3}
      sx={{
        width: isSmallScreen ? "100%" : MIN_CONTROL_CARD_WIDTH,
        p: 2,
        bgcolor: "background.paper",
        display: "flex",
        flexDirection: "column",
        gap: 2,
        flexShrink: 0,
        maxHeight: isSmallScreen ? undefined : "100%",
        overflow: "auto",
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
        }}
      >
        <Typography
          variant="subtitle1"
          sx={{
            fontSize: "1.1rem",
            fontWeight: 500,
            flexGrow: 1,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {`Camera ${selectedCamera.id}`}
        </Typography>
        <TextField
          select
          label="Mode"
          value={mode}
          onChange={(e) => {
            dispatch(setMode(e.target.value as Mode));
          }}
          size="small"
          sx={{
            minWidth: 120,
            "& .MuiOutlinedInput-root": {
              "& fieldset": {
                borderColor: "rgba(255, 255, 255, 0.23)",
              },
              "&:hover fieldset": {
                borderColor: "rgba(255, 255, 255, 0.23)",
              },
              "&.Mui-focused fieldset": {
                borderColor: "primary.main",
              },
            },
            "& .MuiInputLabel-root": {
              color: "rgba(255, 255, 255, 0.7)",
            },
            "& .MuiSelect-icon": {
              color: "rgba(255, 255, 255, 0.7)",
            },
          }}
        >
          {Object.values(Mode).map((option) => (
            <MenuItem key={option} value={option}>
              {option.charAt(0).toUpperCase() + option.slice(1)}
            </MenuItem>
          ))}
        </TextField>
      </Box>
      <PanelFromMode mode={mode} />
    </Paper>
  );
};
export default ControlPanel;
