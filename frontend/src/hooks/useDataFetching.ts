import { useEffect, useRef } from "react";
import { useDispatch } from "react-redux";
import { Input } from "../types/inputs";
import { setCameras } from "../store/DeviceSlice";
import { setRobotPosition, setTags } from "../store/FusedDataSlice";
const FETCH_INTERVAL = 100; // 100ms interval for real-time updates

export const useDataFetching = () => {
  const dispatch = useDispatch();
  const previousDataRef = useRef<string | null>(null); // Ref to store the previous JSON string

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/data");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const input: Input = await response.json();

        // Serialize the fetched data into a string
        const currentDataString = JSON.stringify(input);

        // Compare the new JSON string with the previous one
        if (previousDataRef.current !== currentDataString) {
          // Update the previous data string
          previousDataRef.current = currentDataString;

          // Dispatch actions only if the data has changed
          dispatch(setCameras(input.cameras));
          dispatch(setRobotPosition(input.fused_data.robot_position));
          dispatch(setTags(input.fused_data.targets.april_tags));
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    // Initial fetch
    fetchData();

    // Set up polling interval
    const intervalId = setInterval(fetchData, FETCH_INTERVAL);

    // Cleanup
    return () => clearInterval(intervalId);
  }, [dispatch]);
};
