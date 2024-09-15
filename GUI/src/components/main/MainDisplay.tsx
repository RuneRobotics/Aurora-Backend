import { Box, styled } from "@mui/material";
import { useSelector } from "react-redux";
import { State } from "../../state/state";
import Camera from "../Camera";
import { LayoutType } from "../../state/slices/LayoutSlice";
import Field from "./field/Field";

const Container = styled(Box, {
  shouldForwardProp: (prop) => prop !== "side",
})<{ side: number }>(({ theme, side }) => ({
  backgroundColor: "green",
  borderRadius: theme.shape.borderRadius,
  margin: 0,
  padding: 2,
  gap: theme.spacing(2),
  display: "flex", // Flexbox layout
  alignItems: "flex-start", // Aligns children at the top
  justifyContent: "flex-end", // Aligns children to the right
  overflow: "hidden", // Prevents overflow
  gridArea: `1 / ${side * 6} / -1 / ${side * -1}`,
}));

const MainDisplay: React.FC = () => {
  const side = useSelector((state: State) => state.layout.screenSide);
  const layoutType = useSelector((state: State) => state.layout.layoutType);
  return (
    <Container side={side}>
      {layoutType === LayoutType.CAM ? <Camera /> : <Field></Field>}{" "}
    </Container>
  );
};
export default MainDisplay;
