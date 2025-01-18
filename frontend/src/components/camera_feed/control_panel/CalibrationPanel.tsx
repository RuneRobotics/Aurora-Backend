import React, { useRef } from "react";
import { Box, Button, IconButton, Tooltip, Typography } from "@mui/material";
import { ChevronLeft, ChevronRight, Download, Trash2 } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { StoreState } from "../../../store";
import { CalibrationState, Mode } from "../../../types/state_types";
import {
  deleteSnapshot,
  getSnapshot,
  navigateImage,
} from "../../../store/LayoutSlice";
import {
  getVideoFeedURL,
  MIN_CALIBRATION_IMAGES,
} from "../../../types/Constants";

const CalibrationPanel: React.FC = () => {
  const dispatch = useDispatch();
  const videoFeedRef = useRef<HTMLImageElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const cameraState = useSelector((state: StoreState) => {
    const slice = state.layout_slice;
    if (
      slice.selectedCamera &&
      slice.selectedCamera.mode === Mode.Calibration
    ) {
      return slice.selectedCamera.cameraState as CalibrationState;
    }
    return undefined;
  });
  if (!cameraState) return <></>;

  const imageCount = cameraState.imageCount;
  const canDelete = imageCount > 0;
  const canDownload = imageCount >= MIN_CALIBRATION_IMAGES;

  const handleNavigateImage = (direction: "prev" | "next") => {
    dispatch(navigateImage(direction));
  };

  const takeSnapshot = () => {
    const canvas = canvasRef.current;
    const videoFeed = videoFeedRef.current;

    if (canvas && videoFeed) {
      const context = canvas.getContext("2d");
      canvas.width = videoFeed.width;
      canvas.height = videoFeed.height;

      // Draw the live feed onto the canvas
      context?.drawImage(videoFeed, 0, 0, videoFeed.width, videoFeed.height);

      // Convert the canvas content to a base64-encoded string
      const snapshot = canvas.toDataURL("image/png");

      // Dispatch the snapshot to the Redux store
      dispatch(getSnapshot(snapshot));
    }
  };

  const handleDelete = () => {
    dispatch(deleteSnapshot());
  };

  const handleFinishCalibration = () => {
    // Trigger calibration finalization logic (e.g., API call or Redux action)
    console.log("Calibration finished!");
  };

  return (
    <>
      <Typography variant="h5" gutterBottom>
        Calibration Panel
      </Typography>

      {/* Live feed */}
      <Box
        sx={{
          width: "100%",
          height: 200,
          overflow: "hidden",
          borderRadius: 1,
          bgcolor: "background.default",
          mb: 2,
        }}
      >
        <img
          ref={videoFeedRef}
          src={getVideoFeedURL(cameraState.currentIndex || 0)}
          alt="Live Feed"
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
          }}
        />
      </Box>

      {/* Current Snapshot */}
      {imageCount > 0 && cameraState.currentIndex !== undefined && (
        <Box
          sx={{
            width: "100%",
            height: 200,
            overflow: "hidden",
            borderRadius: 1,
            bgcolor: "background.default",
            mb: 2,
          }}
        >
          <img
            src={cameraState.calibrationImages[cameraState.currentIndex]}
            alt="Current Calibration Snapshot"
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
            }}
          />
        </Box>
      )}

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 1,
          mt: "auto",
        }}
      >
        <Button variant="contained" onClick={takeSnapshot} sx={{ flexGrow: 1 }}>
          Take Snapshot
        </Button>

        <Tooltip title={canDelete ? "Delete the image" : "No images to delete"}>
          <span>
            <IconButton
              onClick={handleDelete}
              disabled={!canDelete}
              size="small"
            >
              <Trash2 size={20} />
            </IconButton>
          </span>
        </Tooltip>

        <Tooltip
          title={
            canDownload
              ? "Download calibration images"
              : `Need ${MIN_CALIBRATION_IMAGES - imageCount} more images`
          }
        >
          <span>
            <IconButton
              onClick={handleFinishCalibration}
              disabled={!canDownload}
              size="small"
              color="primary"
            >
              <Download size={20} />
            </IconButton>
          </span>
        </Tooltip>
      </Box>

      {/* Navigation */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 2,
          mt: 2,
        }}
      >
        <IconButton onClick={() => handleNavigateImage("prev")} size="small">
          <ChevronLeft size={20} />
        </IconButton>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ minWidth: 80, textAlign: "center" }}
        >
          {imageCount} / {MIN_CALIBRATION_IMAGES}
        </Typography>

        <IconButton onClick={() => handleNavigateImage("next")} size="small">
          <ChevronRight size={20} />
        </IconButton>
      </Box>

      {/* Hidden canvas for capturing snapshots */}
      <canvas ref={canvasRef} style={{ display: "none" }} />
    </>
  );
};

export default CalibrationPanel;
