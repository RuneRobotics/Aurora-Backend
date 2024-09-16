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
import NotesTable from "./NoteAccordion";
import AprilTagTable from "./AprilTagAccordion";

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
        <NotesTable
          selectedCameraDeviceIP={deviceIP}
          selectedCameraIndex={cameraIndex}
        />
        <AprilTagTable
          selectedCameraDeviceIP={deviceIP}
          selectedCameraIndex={cameraIndex}
        />
      </AccordionDetails>
    </Accordion>
  );
};

export default CameraAccordion;
