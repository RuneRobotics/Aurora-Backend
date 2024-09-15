import React, { useEffect, useRef } from "react";
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

interface CameraProps {
  deviceIP: string;
  cameraIndex: number;
}

const Camera: React.FC<CameraProps> = ({
  deviceIP,
  cameraIndex,
}: CameraProps) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    if (videoRef.current) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch((err) => console.error("Error accessing webcam: ", err));
    }
  }, []);

  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            width: "100%",
          }}
        >
          <Typography variant="body1">IP: {deviceIP}</Typography>
          <Typography variant="body1">Index: {cameraIndex}</Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          style={{ width: "100%", borderRadius: "8px" }}
        />
      </AccordionDetails>
    </Accordion>
  );
};

export default Camera;
