import { Robot, SafePose3d } from "../../types/inputs";
import { FIELD_HEIGHT, FIELD_WIDTH } from "./constants";
const drawRotatedRectangle = (
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number,
  theta: number,
  radius: number,
  color: string
) => {
  // Save the current state of the canvas
  ctx.save();

  // Translate to the rectangle's center
  ctx.translate(x, y);

  // Rotate the canvas by the given angle (in radians)
  ctx.rotate(-theta);

  // Draw the rectangle centered at the origin (0, 0)
  ctx.fillStyle = color; // Set fill color (optional)
  ctx.beginPath();
  ctx.roundRect(-width / 2, -height / 2, width, height, radius);
  ctx.closePath();
  ctx.fill();
  // Restore the canvas to its original state
  ctx.restore();
};

const drawRobot = (
  robot: Robot,
  normalX: (xVal: number) => number,
  normalY: (yVal: number) => number,
  ctx: CanvasRenderingContext2D
) => {
  const robotWidth = normalX(0.8);
  const robotLength = normalX(0.8);
  const red = "rgba(77, 14, 14, 1)";
  const blue = "rgba(14, 16, 77, 1)";
  const redBumper = "rgba(210, 38, 38, 1)";
  const blueBumper = "rgba(38, 44, 210, 1)";
  const getBumperSize = (sideSize: number) => sideSize * 1.2;
  drawRotatedRectangle(
    ctx,
    normalX(robot.position.x),
    normalY(robot.position.y),
    getBumperSize(robotWidth),
    getBumperSize(robotLength),
    robot.position.yaw,
    5,
    robot.alliance === "RED" ? redBumper : blueBumper
  );
  drawRotatedRectangle(
    ctx,
    normalX(robot.position.x),
    normalY(robot.position.y),
    robotWidth,
    robotLength,
    robot.position.yaw,
    0,
    robot.alliance === "RED" ? red : blue
  );

  const text = robot.team.toString(); // Convert the number to a string
  ctx.font = "bold 15px Arial"; // Set font size and type
  ctx.fillStyle = "white"; // Set text color to white
  ctx.textAlign = "center"; // Align text horizontally to the center
  ctx.textBaseline = "middle"; // Align text vertically to the middle
  ctx.fillText(text, normalX(robot.position.x), normalY(robot.position.y)); // Draw the text at the given coordina

  ctx.beginPath(); // Start a new path
  ctx.arc(
    normalX(
      robot.position.x + (getBumperSize(0.7) / 2) * Math.cos(robot.position.yaw)
    ),
    normalY(
      robot.position.y + (getBumperSize(0.7) / 2) * Math.sin(robot.position.yaw)
    ),
    5,
    0,
    2 * Math.PI
  ); // x, y, radius, startAngle, endAngle
  ctx.fill(); // Fill the circle
  ctx.strokeStyle = "black";
  ctx.stroke();
};

export function draw(
  ctx: CanvasRenderingContext2D,
  height: number,
  width: number,
  localization: SafePose3d
) {
  const normalX = (xVal: number) => xVal * (width / FIELD_WIDTH);
  const normalY = (yVal: number) => height - yVal * (height / FIELD_HEIGHT);
  // aprilTags.forEach((tag) => {
  //   drawAprilTag(localization, tag, normalX, normalY, ctx);
  // });
  if (localization !== "unknown")
    drawRobot(
      {
        team: 6738,
        alliance: "BLUE",
        position: localization,
      },
      normalX,
      normalY,
      ctx
    );
}
