import React from "react";
import { Toolbar, Typography, IconButton } from "@mui/material";
import { Monitor, Layout } from "lucide-react";

// Define the type for props
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
      {isCanvasView ? <Monitor size={24} /> : <Layout size={24} />}
    </IconButton>
  </Toolbar>
);

export default Header;
