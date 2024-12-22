import { Box, Button, IconButton, Tooltip, Typography } from "@mui/material";
import { ChevronLeft, ChevronRight, Download, Trash2 } from "lucide-react";
import { Mode } from "../../../types";

interface Props {
  mode: Mode;
  calibrationImages: Record<string, string[]>;
  selectedCamera: string | null;
  currentIndex: number;
  takeSnapshot: () => Promise<void>;
  imageCount: number;
  handleDeleteLastImage: () => void;
  handleNavigateImage: (direction: "prev" | "next") => void;
  handleFinishCalibration: () => Promise<void>;
}

const CalibrationPanel: React.FC<Props> = ({
  mode,
  calibrationImages,
  selectedCamera,
  currentIndex,
  takeSnapshot,
  imageCount,
  handleDeleteLastImage,
  handleNavigateImage,
  handleFinishCalibration,
}) => {
  const MIN_CALIBRATION_IMAGES = 24;
  const currentCameraImages = calibrationImages[selectedCamera ?? ""] || [];

  const canDelete = imageCount > 0;
  const canDownload = imageCount >= MIN_CALIBRATION_IMAGES;

  return (
    <>
      {mode === "calibration" && (
        <>
          {currentCameraImages.length > 0 && (
            <Box
              sx={{
                width: "100%",
                height: 200,
                overflow: "hidden",
                borderRadius: 1,
                bgcolor: "background.default",
              }}
            >
              <img
                src={currentCameraImages[currentIndex]}
                alt="Last calibration snapshot"
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
            <Button
              variant="contained"
              onClick={takeSnapshot}
              sx={{ flexGrow: 1 }}
            >
              Take Snapshot
            </Button>

            <Tooltip
              title={canDelete ? "Delete the image" : "No images to delete"}
            >
              <span>
                <IconButton
                  onClick={handleDeleteLastImage}
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

          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 2,
            }}
          >
            <IconButton
              onClick={() => handleNavigateImage("prev")}
              disabled={currentIndex === 0}
              size="small"
            >
              <ChevronLeft size={20} />
            </IconButton>

            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ minWidth: 80, textAlign: "center" }}
            >
              {imageCount} / {MIN_CALIBRATION_IMAGES}
            </Typography>

            <IconButton
              onClick={() => handleNavigateImage("next")}
              disabled={currentIndex === currentCameraImages.length - 1}
              size="small"
            >
              <ChevronRight size={20} />
            </IconButton>
          </Box>
        </>
      )}
    </>
  );
};

export default CalibrationPanel;
