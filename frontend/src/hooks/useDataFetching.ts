import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { setData } from "../store/dataSlice";
import { Data } from "../types";

const FETCH_INTERVAL = 100; // 100ms interval for real-time updates

export const useDataFetching = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/data");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data: Data = await response.json();
        dispatch(setData(data));
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
