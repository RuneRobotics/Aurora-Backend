import React from "react";
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import Camera from "../Camera";

interface CameraProps {
  deviceIP: string;
  cameraIndex: number;
}

const CameraAccordion: React.FC<CameraProps> = ({
  deviceIP,
  cameraIndex,
}: CameraProps) => {
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
        <Camera />
      </AccordionDetails>
    </Accordion>
  );
};

export default CameraAccordion;
