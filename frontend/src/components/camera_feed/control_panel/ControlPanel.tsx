import { Box, MenuItem, Paper, TextField, Typography } from "@mui/material";
import { CameraData, LightingSettings, Mode, modes } from "../../../types";
import TuningPanel from "./TuningPanel";
import CalibrationPanel from "./CalibrationPanel";
import DataPanel from "./DataPanel";

interface Props {
  MIN_CONTROL_CARD_WIDTH: number;
  isSmallScreen: boolean;
  selectedCamera: string | null;
  setMode: React.Dispatch<React.SetStateAction<Mode>>;
  mode: Mode;
  camera: CameraData;
  settings: LightingSettings;
  handleTuningChange: (
    setting: "exposure" | "brightness"
  ) => (_event: Event, value: number | number[]) => void;
  calibrationImages: Record<string, string[]>;
  currentIndex: number;
  takeSnapshot: () => Promise<void>;
  imageCount: number;
  handleDeleteLastImage: () => void;
  handleNavigateImage: (direction: "prev" | "next") => void;
  handleFinishCalibration: () => Promise<void>;
}
const ControlPanel: React.FC<Props> = ({
  MIN_CONTROL_CARD_WIDTH,
  isSmallScreen,
  selectedCamera,
  setMode,
  mode,
  camera,
  settings,
  handleTuningChange,
  calibrationImages,
  currentIndex,
  takeSnapshot,
  imageCount,
  handleDeleteLastImage,
  handleNavigateImage,
  handleFinishCalibration,
}: Props) => {
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
          {selectedCamera
            ? `Camera ${selectedCamera.split("-camera-")[1]}`
            : "Camera"}
        </Typography>
        <TextField
          select
          label="Mode"
          value={mode}
          onChange={(e) => setMode(e.target.value as Mode)}
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
          {modes.map((option) => (
            <MenuItem key={option} value={option}>
              {option.charAt(0).toUpperCase() + option.slice(1)}
            </MenuItem>
          ))}
        </TextField>
      </Box>

      <DataPanel mode={mode} camera={camera} />

      <TuningPanel
        mode={mode}
        settings={settings}
        handleTuningChange={handleTuningChange}
      />

      <CalibrationPanel
        mode={mode}
        calibrationImages={calibrationImages}
        selectedCamera={selectedCamera}
        currentIndex={currentIndex}
        takeSnapshot={takeSnapshot}
        imageCount={imageCount}
        handleDeleteLastImage={handleDeleteLastImage}
        handleNavigateImage={handleNavigateImage}
        handleFinishCalibration={handleFinishCalibration}
      />
    </Paper>
  );
};
export default ControlPanel;
