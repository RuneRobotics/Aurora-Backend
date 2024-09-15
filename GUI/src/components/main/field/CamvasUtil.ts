import { Robot } from "../../../state/slices/DataSlice";
import { FIELD_HEIGHT, FIELD_WIDTH } from "./consants";
const drawRobot = (
  robot: Robot,
  normalX: (xVal: number) => number,
  normalY: (yVal: number) => number,
  ctx: CanvasRenderingContext2D
) => {
  const radius = Math.sqrt(robot.width ** 2 + robot.length ** 2) / 2;

  ctx.beginPath();
  const angleToCorner = Math.atan(robot.width / robot.length);
  ctx.moveTo(
    normalX(robot.x + Math.cos(-angleToCorner + robot.rotation) * radius),
    normalY(robot.y + Math.sin(-angleToCorner + robot.rotation) * radius)
  );
  ctx.lineTo(
    normalX(robot.x + Math.cos(angleToCorner + robot.rotation) * radius),
    normalY(robot.y + Math.sin(angleToCorner + robot.rotation) * radius)
  );
  ctx.lineTo(
    normalX(
      robot.x + Math.cos(Math.PI - angleToCorner + robot.rotation) * radius
    ),
    normalY(
      robot.y + Math.sin(Math.PI - angleToCorner + robot.rotation) * radius
    )
  );
  ctx.lineTo(
    normalX(
      robot.x + Math.cos(angleToCorner - Math.PI + robot.rotation) * radius
    ),
    normalY(
      robot.y + Math.sin(angleToCorner - Math.PI + robot.rotation) * radius
    )
  );
  ctx.lineTo(
    normalX(robot.x + Math.cos(-angleToCorner + robot.rotation) * radius),
    normalY(robot.y + Math.sin(-angleToCorner + robot.rotation) * radius)
  );
  ctx.stroke();
};
export function draw(
  ctx: CanvasRenderingContext2D,
  height: number,
  width: number
) {
  const normalX = (xVal: number) => xVal * (width / FIELD_WIDTH);
  const normalY = (yVal: number) => height - yVal * (height / FIELD_HEIGHT);
}
