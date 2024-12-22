import { Box } from "@mui/material";
import React from "react";

const Canvas: React.FC = () => {
  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        padding: 5,
      }}
    >
      <canvas
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "white",
          border: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      />
    </Box>
  );
};
export default Canvas;
