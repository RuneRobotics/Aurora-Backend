import React from "react";
import { Provider } from "react-redux";
import { ThemeProvider, CssBaseline } from "@mui/material";
import { store } from "./store";
import darkTheme from "./themes/darkTheme";
import Dashboard from "./components/Dashboard";

const App: React.FC = () => (
  <Provider store={store}>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Dashboard />
    </ThemeProvider>
  </Provider>
);

export default App;
