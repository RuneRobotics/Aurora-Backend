import { AprilTag, Note, Pose2d, Robot } from "../../types";
import { getTagPose } from "../../utils/AprilTag";
import { FIELD_HEIGHT, FIELD_WIDTH } from "./consants";

function drawNote(
  note: Note,
  ctx: CanvasRenderingContext2D,
  normalX: (xVal: number) => number,
  normalY: (yVal: number) => number
) {
  const centerX = normalX(note.position.x);
  const centerY = normalY(note.position.y);
  const outerRadius = normalX(0.18);
  const innerRadius = normalX(0.135); // Set a smaller radius for the empty circle

  // Draw the outer filled circle
  ctx.fillStyle = "orange";
  ctx.beginPath();
  ctx.arc(centerX, centerY, outerRadius, 0, Math.PI * 2);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.arc(centerX, centerY, innerRadius, 0, Math.PI * 2);
  ctx.closePath();
  ctx.fill();
}
const drawAprilTag = (
  location: { x: number; y: number },
  tag: AprilTag,
  normalX: (xVal: number) => number,
  normalY: (yVal: number) => number,
  ctx: CanvasRenderingContext2D
) => {
  const width = 0.4;
  const length = 0.07;
  const radius = Math.sqrt(width ** 2 + length ** 2) / 2;
  const position: Pose2d | null = getTagPose(tag.id);
  if (position === null) return;
  const drawRectangle = (
    x: number,
    y: number,
    rotation: number,
    color: string,
    radius: number
  ) => {
    const angleToCorner = Math.atan(width / length);
    ctx.fillStyle = color;
    ctx.beginPath();

    const corners = [
      -angleToCorner,
      angleToCorner,
      Math.PI - angleToCorner,
      Math.PI + angleToCorner,
    ].map((cornerAngle) => ({
      x: normalX(x + Math.cos(cornerAngle + rotation) * radius),
      y: normalY(y + Math.sin(cornerAngle + rotation) * radius),
    }));

    ctx.moveTo(corners[0].x, corners[0].y);
    corners.forEach((corner) => ctx.lineTo(corner.x, corner.y));
    ctx.closePath();
    ctx.fill();
  };
  ctx.strokeStyle = "cyan";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(normalX(location.x), normalY(location.y));
  ctx.lineTo(normalX(position.x), normalY(position.y));
  ctx.stroke();
  ctx.beginPath();
  drawRectangle(position.x, position.y, position.yaw, "grey", radius);
  drawRectangle(position.x, position.y, position.yaw, "black", radius * 0.7);
};
const drawRobot = (
  robot: Robot,
  normalX: (xVal: number) => number,
  normalY: (yVal: number) => number,
  ctx: CanvasRenderingContext2D
) => {
  const drawRectangle = (
    x: number,
    y: number,
    width: number,
    length: number,
    rotation: number,
    color: string
  ) => {
    const radius = Math.sqrt(width ** 2 + length ** 2) / 2;
    const angleToCorner = Math.atan(width / length);
    ctx.fillStyle = color;
    ctx.beginPath();

    const corners = [
      -angleToCorner,
      angleToCorner,
      Math.PI - angleToCorner,
      Math.PI + angleToCorner,
    ].map((cornerAngle) => ({
      x: normalX(x + Math.cos(cornerAngle + rotation) * radius),
      y: normalY(y + Math.sin(cornerAngle + rotation) * radius),
    }));

    ctx.moveTo(corners[0].x, corners[0].y);
    corners.forEach((corner) => ctx.lineTo(corner.x, corner.y));
    ctx.closePath();
    ctx.fill();

    // Set the text alignment and baseline
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = robot.alliance === "RED" ? "red" : "blue"; // Set the text color

    // Calculate the available space in the inner rectangle
    const availableWidth = Math.abs(
      normalX(x + width / 2) - normalX(x - width / 2)
    );
    const availableHeight = Math.abs(
      normalY(y + length / 2) - normalY(y - length / 2)
    );

    // Start with the initial font size (14px) and measure the text
    let fontSize = 14;
    ctx.font = `${fontSize}px Arial`;
    let textWidth = ctx.measureText(`${robot.team}`).width;

    // Reduce the font size if the text is too wide for the available width
    while (textWidth > availableWidth && fontSize > 1) {
      fontSize -= 1;
      ctx.font = `${fontSize}px Arial`;
      textWidth = ctx.measureText(`${robot.team}`).width;
    }

    // Also ensure that the font size doesn't exceed the available height
    while (fontSize > availableHeight && fontSize > 1) {
      fontSize -= 1;
      ctx.font = `${fontSize}px Arial`;
    }

    // Draw the text
    ctx.fillText(
      `${robot.team}`,
      normalX(robot.position.x),
      normalY(robot.position.y)
    );
  };

  // Draw the original rectangle
  drawRectangle(
    robot.position.x,
    robot.position.y,
    1,
    1,
    robot.position.yaw,
    robot.alliance
  );

  // Calculate the smaller rectangle dimensions (20% smaller)
  const smallerWidth = 0.8;
  const smallerLength = 0.8;

  // Draw the smaller rectangle inside, with black color
  drawRectangle(
    robot.position.x,
    robot.position.y,
    smallerWidth,
    smallerLength,
    robot.position.yaw,
    "black"
  );
};

export function draw(
  ctx: CanvasRenderingContext2D,
  height: number,
  width: number,
  aprilTags: AprilTag[],
  robots: Robot[],
  notes: Note[],
  localization: Pose2d
) {
  const normalX = (xVal: number) => xVal * (width / FIELD_WIDTH);
  const normalY = (yVal: number) => height - yVal * (height / FIELD_HEIGHT);

  notes.forEach((note) => {
    drawNote(note, ctx, normalX, normalY);
  });

  robots.forEach((robot) => {
    drawRobot(robot, normalX, normalY, ctx);
  });
  // aprilTags.forEach((tag) => {
  //   drawAprilTag(localization, tag, normalX, normalY, ctx);
  // });
  drawRobot(
    {
      team: 6738,
      alliance: "BLUE",
      position: {
        x: localization.x,
        y: localization.y,
        yaw: localization.yaw,
      },
      certainty: 0,
    },
    normalX,
    normalY,
    ctx
  );
}
