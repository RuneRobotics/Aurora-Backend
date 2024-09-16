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
          backgroundColor: "black",
        }}
      >
        <Typography variant="h5" color="white">
          Device IP: {IP}
        </Typography>
      </AccordionSummary>
      <AccordionDetails
        sx={{
          backgroundColor: "black",
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
