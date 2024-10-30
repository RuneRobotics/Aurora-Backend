import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { AprilTag, setPosition, setTags } from "../state/slices/DataSlice";
import { AppDispatch } from "../state/store";

const useFetchData = () => {
  const dispatch: AppDispatch = useDispatch();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/data");
        const data = await response.json();

        const { pose, aprilTags } = data;
        let m_aprilTags: AprilTag[];
        m_aprilTags = aprilTags.map((tag: { id: number }) => ({ id: tag.id }));
        dispatch(setPosition(pose));
        dispatch(setTags(m_aprilTags));
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };

    // Fetch immediately on component mount
    fetchData();

    // Set up interval to fetch data every 5 seconds (5000 ms)
    const intervalId = setInterval(fetchData, 10);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, [dispatch]);
};

export default useFetchData;
