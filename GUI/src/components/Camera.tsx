import React, { useEffect, useRef } from "react";

const Camera: React.FC = () => {
  return <></>;
};
// const Camera: React.FC = () => {
//   const videoRef = useRef<HTMLVideoElement | null>(null);

//   useEffect(() => {
//     if (videoRef.current) {
//       navigator.mediaDevices
//         .getUserMedia({ video: true })
//         .then((stream) => {
//           if (videoRef.current) {
//             videoRef.current.srcObject = stream;
//           }
//         })
//         .catch((err) => console.error("Error accessing webcam: ", err));
//     }
//   }, []);

//   return (
//     <video
//       ref={videoRef}
//       autoPlay
//       playsInline
//       style={{
//         width: "100%", // Makes the video fill the container's width
//         height: "100%", // Makes the video fill the container's height
//         objectFit: "contain", // Ensures video maintains aspect ratio and doesn't overflow
//         borderRadius: "8px",
//       }}
//     />
//   );
// };

export default Camera;
