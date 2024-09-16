import { createTheme } from "@mui/material";

export const darkTheme = createTheme({
  palette: {
    mode: "dark",
    background: {
      default: "#121212", // Dark background
      paper: "#1e1e1e", // Paper background for tables and accordions
    },
    text: {
      primary: "#ffffff", // Light text
    },
  },
});
