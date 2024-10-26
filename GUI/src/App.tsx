import { Provider } from "react-redux";
import Dashboard from "./pages/Dashboard";
import { store } from "./state/store";
import { ThemeProvider } from "@emotion/react";
import { darkTheme } from "./components/theme";
import useFetchData from "./hooks/useFetchData";

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={darkTheme}>
        {/* Render FetchDataWrapper to trigger data fetching */}
        <FetchDataWrapper />
        <Dashboard />
      </ThemeProvider>
    </Provider>
  );
}

// Define the FetchDataWrapper component
function FetchDataWrapper() {
  useFetchData(); // Call the custom hook to fetch data
  return null; // No UI elements need to be rendered
}

export default App;
