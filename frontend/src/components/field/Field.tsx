import React, { useEffect, useRef, useState } from "react";
import { draw } from "./CamvasUtil";
import backgroundImageSrc from "../../assets/image.png";
import FieldContainer from "./Container";
import { aspectRatio as ASPECT_RATIO } from "./consants";
import { useSelector } from "react-redux";
import { StoreState } from "../../store";

const Field: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [backgroundImage, setBackgroundImage] =
    useState<HTMLImageElement | null>(null);
  const data = useSelector((state: StoreState) => state.data);

  // Load the background image on mount
  useEffect(() => {
    const img = new Image();
    img.src = backgroundImageSrc;
    img.onload = () => setBackgroundImage(img);
  }, []);

  // Resize canvas according to the parent's size and aspect ratio
  const resizeCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const { clientWidth: parentWidth, clientHeight: parentHeight } =
      canvas.parentElement ?? { clientWidth: 0, clientHeight: 0 };

    const width =
      parentWidth / parentHeight > ASPECT_RATIO
        ? parentHeight * ASPECT_RATIO
        : parentWidth;

    const height =
      parentWidth / parentHeight > ASPECT_RATIO
        ? parentHeight
        : parentWidth / ASPECT_RATIO;

    // Set canvas dimensions
    canvas.width = width;
    canvas.height = height;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
  };

  // Render and resize canvas on component updates
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !backgroundImage) return;

    const context = canvas.getContext("2d");
    let animationFrameId: number;

    const drawFrame = () => {
      if (context) {
        const { width, height } = canvas;
        context.clearRect(0, 0, width, height);
        context.drawImage(backgroundImage, 0, 0, width, height);

        // Draw additional elements on canvas
        draw(
          context,
          height,
          width,
          data.data?.fused_data.targets.apriltags != null
            ? data.data?.fused_data.targets.apriltags
            : [],
          data.data?.fused_data.targets.robots != null
            ? data.data?.fused_data.targets.robots
            : [],
          data.data?.fused_data.targets.notes != null
            ? data.data?.fused_data.targets.notes
            : [],
          data.data?.fused_data.position != null
            ? data.data?.fused_data.position
            : { x: 0, y: 0, yaw: 0 }
        );
      }
      animationFrameId = requestAnimationFrame(drawFrame);
    };

    const resizeAndDraw = () => {
      resizeCanvas();
      drawFrame();
    };

    resizeAndDraw();
    window.addEventListener("resize", resizeAndDraw);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", resizeAndDraw);
    };
  }, [
    backgroundImage,
    data.data?.fused_data.targets.apriltags != null
      ? data.data?.fused_data.targets.apriltags
      : [],
    data.data?.fused_data.targets.robots != null
      ? data.data?.fused_data.targets.robots
      : [],
    data.data?.fused_data.targets.notes != null
      ? data.data?.fused_data.targets.notes
      : [],
    data.data?.fused_data.position != null
      ? data.data?.fused_data.position
      : { x: 0, y: 0, yaw: 0 },
  ]);
  return (
    <FieldContainer>
      <canvas ref={canvasRef} />
    </FieldContainer>
  );
};

export default Field;
