import React from "react";
import { Box } from "@mui/material";
import { styled } from "@mui/system";
import SideCams from "../components/side_cams/SideCams";
const Item = styled(Box)(({ theme }) => ({
  backgroundColor: "white",
  borderRadius: theme.shape.borderRadius,
  margin: 0,
  padding: 0,
  gap: theme.spacing(2),
}));

export const DashBoardGrid = styled(Box)(() => ({
  height: "100vh",
  width: "100vw",
  backgroundColor: "rgb(13,17,23)",
  color: "#fff",
  display: "grid",
  gridTemplateRows: "repeat(20, 1fr)",
  gridTemplateColumns: "repeat(20, 1fr)",
  gridGap: "1em",
  margin: 0,
  padding: 0,
}));

const DashBoard: React.FC = () => {
  return (
    <DashBoardGrid>
      <SideCams></SideCams>
    </DashBoardGrid>
  );
};

export default DashBoard;
