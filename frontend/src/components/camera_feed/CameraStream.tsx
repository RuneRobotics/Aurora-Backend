import Box from "@mui/material/Box";
import {
  getVideoFeedURL,
  MIN_CONTROL_CARD_WIDTH,
  MIN_FEED_HEIGHT,
} from "../../types/Constants";
import { useSelector } from "react-redux";
import { StoreState } from "../../store";

export interface Props {
  isSmallScreen: boolean;
  canvasRef: React.RefObject<HTMLCanvasElement>;
}

const CameraStream: React.FC<Props> = ({ isSmallScreen, canvasRef }: Props) => {
  const cameraIndex = useSelector((state: StoreState) => {
    state.layout_slice.selectedCamera?.id;
  });
  if (cameraIndex === undefined) return <></>;
  return (
    <Box
      sx={{
        flexGrow: 1,
        minHeight: MIN_FEED_HEIGHT,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        minWidth: isSmallScreen ? "100%" : MIN_CONTROL_CARD_WIDTH,
        position: "relative",
      }}
    >
      <img
        src={getVideoFeedURL(cameraIndex)}
        alt="Camera Feed"
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
        }}
      />
      <canvas ref={canvasRef} style={{ display: "none" }} />
    </Box>
  );
};
export default CameraStream;
