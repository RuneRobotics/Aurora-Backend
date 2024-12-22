import { Box } from "@mui/material";
import { styled } from "@mui/system";

const FieldContainer = styled(Box)(({ theme }) => ({
  backgroundColor: "rgb(12,21,36)",
  borderRadius: theme.shape.borderRadius,
  margin: 0,
  padding: 0,
  textAlign: "center",
  width: "100%",
  height: "100%",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}));
export default FieldContainer;
