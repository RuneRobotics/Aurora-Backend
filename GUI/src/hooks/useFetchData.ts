import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { setPosition, setTags } from "../state/slices/DataSlice";
import { AppDispatch } from "../state/store";

const useFetchData = () => {
  const dispatch: AppDispatch = useDispatch();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/data");
        const data = await response.json();

        const { pose } = data;
        dispatch(setPosition(pose));
        dispatch(setTags([]));
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };

    // Fetch immediately on component mount
    fetchData();

    // Set up interval to fetch data every 5 seconds (5000 ms)
    const intervalId = setInterval(fetchData, 50);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, [dispatch]);
};

export default useFetchData;
