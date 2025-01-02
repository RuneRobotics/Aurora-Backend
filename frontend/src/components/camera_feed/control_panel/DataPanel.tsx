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
} from "@mui/material";
import { useState } from "react";
import { TargetType } from "../../../types/Constants";
import { targets } from "../../../types/inputs";
import { useSelector } from "react-redux";
import { StoreState } from "../../../store";
function getAttributes(targetType: TargetType) {
  switch (targetType) {
    case TargetType.AprilTag:
      console.log("hi");
      return ["id", "distance"];
  }
  return [];
}

const DataPanel: React.FC = () => {
  const [targetType, setTargetType] = useState<TargetType>(TargetType.AprilTag);
  const targets: undefined | targets = useSelector((state: StoreState) => {
    let cameraIndex: undefined | number = undefined;
    const id = state.layout_slice.selectedCamera?.id;
    if (id) {
      cameraIndex = state.device_slice.cameras.findIndex(
        (camera) => camera.camera_id === id
      );
    }
    if (cameraIndex === undefined) {
      return undefined;
    }
    return state.device_slice.cameras[cameraIndex].targets;
  });
  console.log("rendered");

  if (targets)
    return (
      <Stack>
        <TextField
          select
          label="Target"
          value={targetType}
          onChange={(e) => {
            console.log("pizza");
            setTargetType(e.target.value as TargetType);
          }}
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
          {Object.keys(targets).map((option) => (
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
              {targets[targetType].map((target, index) => {
                const targetAttrs = Object.keys(target);
                return (
                  <TableRow key={index}>
                    {getAttributes(targetType).map((attr: string, index) => {
                      console.log(attr);
                      if (targetAttrs.includes(attr)) {
                        console.log(attr);
                        return (
                          <TableCell key={index}>
                            {
                              target[attr as keyof typeof target] as
                                | number
                                | string
                            }
                          </TableCell>
                        );
                      } /* else if (
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
                        }*/
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
