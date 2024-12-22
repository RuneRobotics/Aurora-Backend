import { useState } from "react";

const useResizableSidebar = (initialWidth: number) => {
  const [sidebarWidth, setSidebarWidth] = useState(initialWidth);
  const [isResizing, setIsResizing] = useState(false);

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsResizing(true);
    e.preventDefault();
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isResizing) return;

    const maxWidth = window.innerWidth * 0.3;
    const minWidth = window.innerWidth * 0.2;
    const newWidth = window.innerWidth - e.clientX;

    if (newWidth >= minWidth && newWidth <= maxWidth) setSidebarWidth(newWidth);
    else if (newWidth < minWidth / 2) setSidebarWidth(0);
    else if (newWidth < minWidth) setSidebarWidth(minWidth);
    else if (newWidth > maxWidth) setSidebarWidth(maxWidth);
  };

  const handleMouseUp = () => {
    setIsResizing(false);
    if (sidebarWidth < window.innerWidth * 0.2)
      setSidebarWidth(
        sidebarWidth < window.innerWidth * 0.1 ? 0 : window.innerWidth * 0.2
      );
  };

  return {
    sidebarWidth,
    isResizing,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
  };
};

export default useResizableSidebar;
