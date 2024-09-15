import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
} from "@mui/material";
import { Device } from "../../state/slices/CameraSlice";
import Camera from "./Camera";

const DeviceDisplay: React.FC<Device> = ({ IP, cameraAmount }: Device) => {
  return (
    <Accordion>
      <AccordionSummary
        sx={{
          backgroundColor: "green",
        }}
      >
        <Typography variant="h5">Device IP: {IP}</Typography>
      </AccordionSummary>
      <AccordionDetails
        sx={{
          backgroundColor: "green",
        }}
      >
        {Array.from({ length: cameraAmount }, (_, index) => (
          <Camera key={index} cameraIndex={index} deviceIP={IP} />
        ))}
      </AccordionDetails>
    </Accordion>
  );
};
export default DeviceDisplay;
