import { Box, Slider, Typography } from "@mui/material";
import { LightingSettings, Mode } from "../../../types";
interface Props {
  mode: Mode;
  settings: LightingSettings;
  handleTuningChange: (
    setting: "exposure" | "brightness"
  ) => (_event: Event, value: number | number[]) => void;
}

const TuningPanel: React.FC<Props> = ({
  mode,
  settings,
  handleTuningChange,
}: Props) => {
  if (mode === "tuning" && settings)
    return (
      <Box sx={{ flex: 1 }}>
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom color="text.secondary">
            Exposure ({settings.exposure}%)
          </Typography>
          <Slider
            value={settings.exposure}
            onChange={handleTuningChange("exposure")}
            min={0}
            max={100}
            valueLabelDisplay="auto"
          />
        </Box>
        <Box>
          <Typography gutterBottom color="text.secondary">
            Brightness ({settings.brightness}%)
          </Typography>
          <Slider
            value={settings.brightness}
            onChange={handleTuningChange("brightness")}
            min={0}
            max={100}
            valueLabelDisplay="auto"
          />
        </Box>
      </Box>
    );

  return <></>;
};
export default TuningPanel;
