import Box from "@mui/material/Box";

export interface Props {
  MIN_FEED_HEIGHT: string;
  MIN_CONTROL_CARD_WIDTH: number;
  isSmallScreen: boolean;
  VIDEO_FEED_URL: string;
  canvasRef: React.RefObject<HTMLCanvasElement>;
}

const CameraStream: React.FC<Props> = ({
  MIN_CONTROL_CARD_WIDTH,
  MIN_FEED_HEIGHT,
  isSmallScreen,
  VIDEO_FEED_URL,
  canvasRef,
}: Props) => {
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
