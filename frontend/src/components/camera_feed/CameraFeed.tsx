import { Box, Typography } from "@mui/material";
import CameraStream from "./CameraStream";
import ControlPanel from "./control_panel/ControlPanel";
import { useSelector } from "react-redux";
import { StoreState } from "../../store";

import { useMediaQuery, useTheme } from "@mui/material";

import { useRef } from "react";

const CameraFeed: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));
  const isCameraSelected = useSelector(
    (state: StoreState) => state.layout_slice.selectedCamera !== undefined
  );
  if (!isCameraSelected) {
    return (
      <Box
        sx={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          bgcolor: "background.default",
        }}
      >
        <Typography variant="h5" color="text.secondary">
          Select a camera to view feed
        </Typography>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        bgcolor: "background.default",
        display: "flex",
        flexDirection: isSmallScreen ? "column" : "row",
        gap: 2,
        px: 1,
        py: 2,
        overflow: "auto",
      }}
    >
      <CameraStream
        isSmallScreen={isSmallScreen}
        canvasRef={canvasRef}
      ></CameraStream>
      <ControlPanel isSmallScreen={isSmallScreen}></ControlPanel>
    </Box>
  );
};

export default CameraFeed;
