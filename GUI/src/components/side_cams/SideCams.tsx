import { Box, styled, Typography } from "@mui/material";
import { useSelector } from "react-redux";
import { State } from "../../state/state";
import DeviceDisplay from "./DeviceDisplay";

const Container = styled(Box, {
  shouldForwardProp: (prop) => prop !== "side",
})<{ side: number }>(({ theme, side }) => ({
  backgroundColor: "424242",
  borderRadius: theme.shape.borderRadius,
  margin: 0,
  padding: 0,
  gap: theme.spacing(2),
  gridArea: `1 / ${side * 1} / -1 / ${side * 6}`,
  overflowY: "scroll", // Allows scrolling
  // Hide scrollbar for WebKit browsers (Chrome, Safari)
  "&::-webkit-scrollbar": {
    display: "none",
  },
  // Hide scrollbar for Firefox
  scrollbarWidth: "none",
}));
const SideCams: React.FC = () => {
  const side = useSelector((state: State) => state.layout.screenSide);
  const exist = useSelector((state: State) => state.layout.sideCams);
  const devices = useSelector((state: State) => state.cameras.devices);

  if (exist)
    return (
      <Container side={side}>
        <Typography variant="h3">Devices</Typography>
        {devices.map((device, index) => (
          <DeviceDisplay
            key={index}
            IP={device.IP}
            cameraAmount={device.cameraAmount}
          />
        ))}
      </Container>
    );
  return <></>;
};
export default SideCams;
