import React from "react";
import { Box, CssBaseline } from "@mui/material";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../types";
import { toggleView } from "../store/deviceSlice";
import useResizableSidebar from "../hooks/useResizeableSlider";
import Header from "./Header";
import Sidebar from "./SideBar";
import ResizeHandle from "./ResizeHandler";
import CameraFeed from "./camera_feed/CameraFeed";
import { useDataFetching } from "../hooks/useDataFetching";
import Canvas from "./Canvas";
import Field from "./field/Field";

const Dashboard: React.FC = () => {
  useDataFetching();
  const dispatch = useDispatch();
  const isCanvasView = useSelector(
    (state: RootState) => state.devices.isCanvasView
  );
  const {
    sidebarWidth,
    isResizing,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
  } = useResizableSidebar(window.innerWidth * 0.25);

  return (
    <Box
      sx={{
        display: "flex",
        height: "100vh",
        bgcolor: "background.default",
        cursor: isResizing ? "col-resize" : "auto",
      }}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      <CssBaseline />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          height: "100vh",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          bgcolor: "background.default",
        }}
      >
        <Header
          isCanvasView={isCanvasView}
          toggleView={() => dispatch(toggleView())}
        />
        <Box
          sx={{
            flexGrow: 1,
            overflow: "hidden",
            bgcolor: "background.default",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {isCanvasView ? <Field /> : <CameraFeed />}
        </Box>
      </Box>
      <ResizeHandle onMouseDown={handleMouseDown} isResizing={isResizing} />
      <Sidebar width={sidebarWidth} />
    </Box>
  );
};

export default Dashboard;
