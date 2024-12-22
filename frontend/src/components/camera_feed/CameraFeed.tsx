import React, { useRef, useState, useEffect } from "react";
import { Box, Typography, useTheme, useMediaQuery } from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import JSZip from "jszip";
import { DeviceData, LightingSettings, Mode } from "../../types";
import {
  addCalibrationImage,
  deleteLastCalibrationImage,
  clearCalibrationImages,
  updateTuningSettings,
  navigateCalibrationImage,
} from "../../store/deviceSlice";
import { StoreState } from "../../store";
import CameraStream from "./CameraStream";
import ControlPanel from "./control_panel/ControlPanel";

const MIN_CALIBRATION_IMAGES = 24;
const MIN_CONTROL_CARD_WIDTH = 250;
const MIN_FEED_HEIGHT = "50vh";
const VIDEO_FEED_URL = "http://localhost:5001/video_feed";

const CameraFeed: React.FC = () => {
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("md"));
  const selectedCamera = useSelector(
    (state: StoreState) => state.devices.selectedCamera
  );
  const data = useSelector((state: StoreState) => state.data.data);
  const calibrationImages = useSelector(
    (state: StoreState) => state.devices.calibrationImages
  );
  const currentImageIndex = useSelector(
    (state: StoreState) => state.devices.currentImageIndex
  );
  const tuningSettings = useSelector(
    (state: StoreState) => state.devices.tuningSettings
  );
  const isCanvasView = useSelector(
    (state: StoreState) => state.devices.isCanvasView
  );
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);
  const [mode, setMode] = useState<Mode>("data");
  const dispatch = useDispatch();

  const findSelectedCamera = () => {
    if (!data || !selectedCamera) return null;

    const [deviceId, cameraIndex] = selectedCamera.split("-camera-");
    const device = data.devices.find((d: DeviceData) => d.id === deviceId);
    if (!device) return null;

    return device.cameras[parseInt(cameraIndex)];
  };

  const camera = findSelectedCamera();
  const imageCount = camera
    ? calibrationImages[selectedCamera ?? ""]?.length || 0
    : 0;
  const currentIndex = camera
    ? currentImageIndex[selectedCamera ?? ""] || 0
    : 0;
  const settings: LightingSettings = camera
    ? tuningSettings[selectedCamera ?? ""]
    : null;

  useEffect(() => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    imgRef.current = img; //it says cannot assign to currebbt because it is a read only property, what should i do?
  }, []);

  const takeSnapshot = async () => {
    if (!canvasRef.current || !selectedCamera) return;

    try {
      const img = new Image();
      img.crossOrigin = "anonymous";

      const imageLoaded = new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = VIDEO_FEED_URL;
      });

      await imageLoaded;

      const canvas = canvasRef.current;
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext("2d");

      if (ctx) {
        ctx.drawImage(img, 0, 0);
        const imageData = canvas.toDataURL("image/jpeg");
        dispatch(addCalibrationImage({ cameraId: selectedCamera, imageData }));
      }
    } catch (error) {
      console.error("Error taking snapshot:", error);
    }
  };

  const handleDeleteLastImage = () => {
    if (selectedCamera && imageCount > 0) {
      dispatch(deleteLastCalibrationImage(selectedCamera));
    }
  };

  const handleFinishCalibration = async () => {
    if (!selectedCamera || !camera || imageCount < MIN_CALIBRATION_IMAGES)
      return;

    const zip = new JSZip();
    const images = calibrationImages[selectedCamera];

    images.forEach((imageData, index) => {
      const data = imageData.split(",")[1];
      zip.file(`image_${index + 1}.jpg`, data, { base64: true });
    });

    const blob = await zip.generateAsync({ type: "blob" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = `calibration_camera_${selectedCamera}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
    dispatch(clearCalibrationImages(selectedCamera));
  };

  const handleTuningChange =
    (setting: "exposure" | "brightness") =>
    (_event: Event, value: number | number[]) => {
      if (selectedCamera && typeof value === "number") {
        dispatch(
          updateTuningSettings({
            cameraId: selectedCamera,
            setting,
            value,
          })
        );
      }
    };

  const handleNavigateImage = (direction: "prev" | "next") => {
    if (selectedCamera) {
      dispatch(
        navigateCalibrationImage({ cameraId: selectedCamera, direction })
      );
    }
  };

  if (isCanvasView) {
    return (
      <Box
        sx={{
          width: "100%",
          height: "100%",
          bgcolor: "background.default",
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "flex-start",
        }}
      >
        <canvas id="dataCanvas" style={{ width: "100%", height: "100%" }} />
      </Box>
    );
  }

  if (!camera) {
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
        MIN_CONTROL_CARD_WIDTH={MIN_CALIBRATION_IMAGES}
        canvasRef={canvasRef}
        MIN_FEED_HEIGHT={MIN_FEED_HEIGHT}
        isSmallScreen={isSmallScreen}
        VIDEO_FEED_URL={VIDEO_FEED_URL}
      ></CameraStream>
      <ControlPanel
        MIN_CONTROL_CARD_WIDTH={MIN_CONTROL_CARD_WIDTH}
        isSmallScreen={isSmallScreen}
        selectedCamera={null}
        setMode={setMode}
        mode={mode}
        camera={camera}
        settings={settings}
        handleTuningChange={handleTuningChange}
        calibrationImages={calibrationImages}
        currentIndex={currentIndex}
        takeSnapshot={takeSnapshot}
        imageCount={imageCount}
        handleDeleteLastImage={handleDeleteLastImage}
        handleNavigateImage={handleNavigateImage}
        handleFinishCalibration={handleFinishCalibration}
      ></ControlPanel>
    </Box>
  );
};

export default CameraFeed;
