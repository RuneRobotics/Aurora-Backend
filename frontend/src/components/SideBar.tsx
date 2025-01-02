import React from "react";
import { Box, Toolbar, Typography } from "@mui/material";
import DeviceList from "./DeviceList";

interface SidebarProps {
  width: number;
}

const Sidebar: React.FC<SidebarProps> = ({ width }) => (
  <Box
    component="nav"
    sx={{
      width,
      flexShrink: 0,
      borderLeft: "1px solid rgba(255, 255, 255, 0.12)",
      bgcolor: "background.paper",
      height: "100vh",
      overflow: "auto",
      transition: "width 0.2s ease",
    }}
  >
    <Toolbar>
      <Typography variant="h6" sx={{ color: "common.white" }}>
        Device
      </Typography>
    </Toolbar>
    <DeviceList />
  </Box>
);

export default Sidebar;
