import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
} from "@mui/material";
import { Device } from "../../state/slices/CameraSlice";
import CameraAccordion from "./CamerAccordion";

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
          <CameraAccordion key={index} cameraIndex={index} deviceIP={IP} />
        ))}
      </AccordionDetails>
    </Accordion>
  );
};
export default DeviceDisplay;
