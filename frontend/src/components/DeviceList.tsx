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
import { DeviceData, RootState } from "../types";
import { setSelectedCamera } from "../store/deviceSlice";
import { StoreState } from "../store";

const DeviceList: React.FC = () => {
  const data = useSelector((state: StoreState) => state.data.data);
  const selectedCamera = useSelector(
    (state: RootState) => state.devices.selectedCamera
  );
  const dispatch = useDispatch();

  if (!data) {
    return (
      <Box sx={{ p: 2 }}>
        <Typography color="text.secondary">No data available</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: "100%", p: 1 }}>
      {data.devices.map((device: DeviceData) => (
        <Accordion
          key={device.id}
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
                {device.name}
              </Typography>
              <Typography
                variant="caption"
                color="text.secondary"
                sx={{
                  flexShrink: 0,
                  ml: 1,
                }}
              >
                ({device.ipAddress})
              </Typography>
            </Box>
          </AccordionSummary>
          <AccordionDetails sx={{ p: 1 }}>
            {device.cameras.map((_camera, index) => (
              <Button
                key={`${device.id}-camera-${index}`}
                onClick={() =>
                  dispatch(setSelectedCamera(`${device.id}-camera-${index}`))
                }
                variant={
                  selectedCamera === `${device.id}-camera-${index}`
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
      ))}
    </Box>
  );
};

export default DeviceList;
