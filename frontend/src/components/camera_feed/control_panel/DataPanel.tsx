import {
  MenuItem,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { CameraData, Mode, targets, TargetType } from "../../../types";
import { formatCameraData } from "../../../utils/formatters";
import { useState } from "react";
interface Props {
  mode: Mode;
  camera: CameraData;
}
function getAttributes(targetType: TargetType) {
  switch (targetType) {
    case "robots":
      return ["team", "certainty", "alliance", "x", "y", "yaw"];
    case "notes":
      return ["x", "y", "certainty"];
    case "apriltags":
    default:
      return ["id", "certainty", "x", "y", "z", "roll", "pitch", "yaw"];
  }
}
const DataPanel: React.FC<Props> = ({ mode, camera }: Props) => {
  const [targetType, setTargetType] = useState<TargetType>("apriltags");
  const data = camera.notes;
  console.log(data);
  if (mode === "data")
    return (
      <Stack>
        <TextField
          select
          label="Target"
          value={targetType}
          onChange={(e) => setTargetType(e.target.value as TargetType)}
          size="small"
          sx={{
            minWidth: 120,
            "& .MuiOutlinedInput-root": {
              "& fieldset": {
                borderColor: "rgba(255, 255, 255, 0.23)",
              },
              "&:hover fieldset": {
                borderColor: "rgba(255, 255, 255, 0.23)",
              },
              "&.Mui-focused fieldset": {
                borderColor: "primary.main",
              },
            },
            "& .MuiInputLabel-root": {
              color: "rgba(255, 255, 255, 0.7)",
            },
            "& .MuiSelect-icon": {
              color: "rgba(255, 255, 255, 0.7)",
            },
          }}
        >
          {targets.map((option) => (
            <MenuItem key={option} value={option}>
              {option.charAt(0).toUpperCase() + option.slice(1)}
            </MenuItem>
          ))}
        </TextField>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                {getAttributes(targetType).map((value, index) => {
                  return <TableCell key={index}>{value}</TableCell>;
                })}
              </TableRow>
            </TableHead>
            <TableBody>
              {data &&
                data.map((target, index) => {
                  const targetAttrs = Object.keys(target);
                  return (
                    <TableRow key={index}>
                      {getAttributes(targetType).map((attr: string, index) => {
                        if (targetAttrs.includes(attr)) {
                          return (
                            <TableCell key={index}>
                              {
                                target[attr as keyof typeof target] as
                                  | number
                                  | string
                              }
                            </TableCell>
                          );
                        } else if (
                          Object.keys(target.position).includes(attr)
                        ) {
                          return (
                            <TableCell key={index}>
                              {
                                target.position[
                                  attr as keyof typeof target.position
                                ] as number
                              }
                            </TableCell>
                          );
                        }
                        return <TableCell key={index}>-</TableCell>;
                      })}
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </TableContainer>
      </Stack>
    );
  return <></>;
};
export default DataPanel;
