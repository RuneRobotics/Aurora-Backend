import React from "react";
import { Toolbar, Typography, IconButton } from "@mui/material";
import MapIcon from "@mui/icons-material/Map";
import CameraAltIcon from "@mui/icons-material/CameraAlt";
import { useDispatch, useSelector } from "react-redux";
import { StoreState } from "../store";
import { toggleView } from "../store/LayoutSlice";
// Use HeaderProps to explicitly type the props in the component
const Header: React.FC = () => {
  const dispatch = useDispatch();
  const view = useSelector((state: StoreState) => state.layout_slice.view);
  return (
    <Toolbar sx={{ bgcolor: "background.paper" }}>
      <Typography
        variant="h6"
        component="div"
        sx={{ flexGrow: 1, color: "common.white" }}
      >
        Aurora Dashboard
      </Typography>
      <IconButton
        onClick={() => dispatch(toggleView())}
        sx={{ color: "common.white" }}
      >
        {view === "Field" ? <MapIcon /> : <CameraAltIcon />}
      </IconButton>
    </Toolbar>
  );
};

export default Header;
