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
import { selectedCamera } from "../../state/slices/CameraSlice";
import { State } from "../../state/state";
import { Note } from "../../state/slices/DataSlice";

// Define the Note interface
export interface CameraNote {
  x: number;
  y: number;
  certainty: number;
}

const NotesTable: React.FC<selectedCamera> = (camera: selectedCamera) => {
  const allNotes: Note[] = useSelector((state: State) => state.data.notes);
  const notes: CameraNote[] = [];

  allNotes.forEach((note) => {
    let flag = false;
    note.cameras.forEach((noteCamera, index) => {
      if (flag) return;
      if (
        noteCamera.camera.selectedCameraDeviceIP ===
          camera.selectedCameraDeviceIP &&
        noteCamera.camera.selectedCameraIndex === camera.selectedCameraIndex
      ) {
        notes.push({
          x: note.x,
          y: note.y,
          certainty: note.cameras[index].certainty,
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
        <Typography>Notes</Typography>
      </AccordionSummary>
      <AccordionDetails
        sx={{
          backgroundColor: "black",
        }}
      >
        <TableContainer component={Paper}>
          {/* Add size="small" for dense table */}
          <Table aria-label="notes table" size="small">
            <TableHead>
              <TableRow>
                <TableCell>X</TableCell>
                <TableCell>Y</TableCell>
                <TableCell>Certainty</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {notes.map((note, index) => (
                <TableRow
                  key={index}
                  sx={{
                    backgroundColor: index % 2 === 0 ? "#424242" : "inherit", // Medium grey for odd rows
                  }}
                >
                  <TableCell>{note.x}</TableCell>
                  <TableCell>{note.y}</TableCell>
                  <TableCell>{note.certainty}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </AccordionDetails>
    </Accordion>
  );
};

export default NotesTable;
