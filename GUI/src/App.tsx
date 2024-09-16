import { Provider } from "react-redux";
import Dashboard from "./pages/Dashboard";
import { store } from "./state/store";
import { ThemeProvider } from "@emotion/react";
import { darkTheme } from "./components/theme";

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={darkTheme}>
        <Dashboard />
      </ThemeProvider>
    </Provider>
  );
}

export default App;
