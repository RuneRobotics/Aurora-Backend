import React from "react";
import { Toolbar, Typography, IconButton } from "@mui/material";
import MapIcon from "@mui/icons-material/Map";
import CameraAltIcon from "@mui/icons-material/CameraAlt";

interface HeaderProps {
  isCanvasView: boolean;
  toggleView: () => void;
}

// Use HeaderProps to explicitly type the props in the component
const Header: React.FC<HeaderProps> = ({ isCanvasView, toggleView }) => (
  <Toolbar sx={{ bgcolor: "background.paper" }}>
    <Typography
      variant="h6"
      component="div"
      sx={{ flexGrow: 1, color: "common.white" }}
    >
      Aurora Dashboard
    </Typography>
    <IconButton onClick={toggleView} sx={{ color: "common.white" }}>
      {isCanvasView ? <MapIcon /> : <CameraAltIcon />}
    </IconButton>
  </Toolbar>
);

export default Header;
