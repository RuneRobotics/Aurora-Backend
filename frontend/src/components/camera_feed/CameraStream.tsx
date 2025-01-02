import Box from "@mui/material/Box";
import {
  MIN_CONTROL_CARD_WIDTH,
  MIN_FEED_HEIGHT,
  VIDEO_FEED_URL,
} from "../../types/Constants";

export interface Props {
  isSmallScreen: boolean;
  canvasRef: React.RefObject<HTMLCanvasElement>;
}

const CameraStream: React.FC<Props> = ({ isSmallScreen, canvasRef }: Props) => {
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
        src={VIDEO_FEED_URL}
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
