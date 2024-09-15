import { Provider } from "react-redux";
import Dashboard from "./pages/Dashboard";
import { store } from "./state/store";

function App() {
  return (
    <Provider store={store}>
      <Dashboard></Dashboard>
    </Provider>
  );
}

export default App;
