import React from "react";
import { Box } from "@mui/material";

interface ResizeHandleProps {
  onMouseDown: (e: React.MouseEvent) => void;
  isResizing: boolean;
}

const ResizeHandle: React.FC<ResizeHandleProps> = ({
  onMouseDown,
  isResizing,
}) => (
  <Box
    sx={{
      width: "4px",
      bgcolor: isResizing ? "primary.main" : "transparent",
      cursor: "col-resize",
      "&:hover": { bgcolor: "primary.main" },
    }}
    onMouseDown={onMouseDown}
  />
);

export default ResizeHandle;
