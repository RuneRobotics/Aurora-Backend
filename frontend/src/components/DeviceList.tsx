import React from "react";
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Button,
  Typography,
} from "@mui/material";
import { ChevronDown, Monitor } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { StoreState } from "../store";
import { UN_DEFINED_IP } from "../types/Constants";
import { setSelectedCameraID } from "../store/LayoutSlice";

const DeviceList: React.FC = () => {
  const device = useSelector((state: StoreState) => state.device_slice);
  const selectedCamera = useSelector((state: StoreState) => {
    const id = state.layout_slice.selectedCamera?.id;
    if (id) {
      return state.device_slice.cameras.find(
        (camera) => camera.camera_id === id
      );
    }
    return undefined;
  });
  const dispatch = useDispatch();

  if (device.ip === UN_DEFINED_IP) {
    return (
      <Box sx={{ p: 2 }}>
        <Typography color="text.secondary">No data available</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: "100%", p: 1 }}>
      <Accordion
        defaultExpanded
        sx={{
          mb: 1,
          "&:before": { display: "none" },
          bgcolor: "background.paper",
          minHeight: 0,
          "& .MuiAccordionSummary-content": {
            margin: "8px 0",
            overflow: "hidden",
          },
        }}
      >
        <AccordionSummary
          expandIcon={<ChevronDown />}
          sx={{
            minHeight: 0,
            borderBottom: "1px solid rgba(255, 255, 255, 0.12)",
            "& .MuiAccordionSummary-content": {
              margin: "8px 0",
            },
          }}
        >
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              minWidth: 0,
              width: "100%",
            }}
          >
            <Monitor size={20} style={{ flexShrink: 0 }} />
            <Typography
              sx={{
                flexGrow: 1,
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              {device.ip}
            </Typography>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{
                flexShrink: 0,
                ml: 1,
              }}
            >
              ({device.ip})
            </Typography>
          </Box>
        </AccordionSummary>
        <AccordionDetails sx={{ p: 1 }}>
          {device.cameras.map((camera, index) => (
            <Button
              key={`${device.ip}-camera-${index}`}
              onClick={() => dispatch(setSelectedCameraID(camera.camera_id))}
              variant={
                selectedCamera?.camera_id === camera.camera_id
                  ? "contained"
                  : "outlined"
              }
              fullWidth
              sx={{ mb: 1, textAlign: "left" }}
            >
              Camera {index + 1}
            </Button>
          ))}
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default DeviceList;
