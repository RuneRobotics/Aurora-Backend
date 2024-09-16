import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Accordion,
  AccordionSummary,
  Typography,
  AccordionDetails,
} from "@mui/material";
import { useSelector } from "react-redux";
import { State } from "../../state/state";
import { AprilTag } from "../../state/slices/DataSlice";
import { selectedCamera } from "../../state/slices/CameraSlice";

// Define the AprilTag interface
export interface CammeraAprilTag {
  id: number;
  x: number;
  y: number;
  z: number;
  roll: number;
  pitch: number;
  yaw: number;
  certainty: number;
}

// Create a dark theme

const AprilTagTable: React.FC<selectedCamera> = (camera: selectedCamera) => {
  const allTags: AprilTag[] = useSelector(
    (state: State) => state.data.aprilTags
  );
  const aprilTags: CammeraAprilTag[] = [];
  allTags.forEach((tag) => {
    let flag = false;
    tag.cameras.forEach((tagCamera, index) => {
      if (flag) return;
      if (
        tagCamera.camera.selectedCameraDeviceIP ===
          camera.selectedCameraDeviceIP &&
        tagCamera.camera.selectedCameraIndex === camera.selectedCameraIndex
      ) {
        aprilTags.push({
          ...tag,
          certainty: tag.cameras[index].certainty,
        });
        flag = true;
      }
    });
  });
  return (
    <Accordion>
      <AccordionSummary
        sx={{
          backgroundColor: "black",
        }}
      >
        <Typography>April Tags</Typography>
      </AccordionSummary>
      <AccordionDetails
        sx={{
          backgroundColor: "black",
        }}
      >
        <TableContainer component={Paper}>
          {/* Add size="small" for dense table */}
          <Table aria-label="april tag table" size="small">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>X</TableCell>
                <TableCell>Y</TableCell>
                <TableCell>Z</TableCell>
                <TableCell>Roll</TableCell>
                <TableCell>Pitch</TableCell>
                <TableCell>Yaw</TableCell>
                <TableCell>Certainty</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {aprilTags.map((tag, index) => (
                <TableRow
                  key={tag.id}
                  sx={{
                    backgroundColor: index % 2 === 0 ? "#424242" : "inherit", // Medium grey for odd rows
                  }}
                >
                  <TableCell>{tag.id}</TableCell>
                  <TableCell>{tag.x}</TableCell>
                  <TableCell>{tag.y}</TableCell>
                  <TableCell>{tag.z}</TableCell>
                  <TableCell>{tag.roll}</TableCell>
                  <TableCell>{tag.pitch}</TableCell>
                  <TableCell>{tag.yaw}</TableCell>
                  <TableCell>{tag.certainty}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </AccordionDetails>
    </Accordion>
  );
};

export default AprilTagTable;
