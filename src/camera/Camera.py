"""
This file is part of HuskyBot CV.
Copyright (C) 2025 Advanced Robotics at the University of Washington <robomstr@uw.edu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from dataclasses import dataclass

import cv2
from line_profiler import profile


@dataclass
class CameraConfig:
    codec: str
    width: int
    height: int
    fps: int
    auto_exposure: int
    exposure: int
    saturation: int
    auto_white_balance: int
    white_balance: int

    def applyConfig(self, camera: cv2.VideoCapture):
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.codec))

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        camera.set(cv2.CAP_PROP_FPS, self.fps)

        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, self.auto_exposure)
        camera.set(cv2.CAP_PROP_EXPOSURE, self.exposure)

        camera.set(cv2.CAP_PROP_SATURATION, self.saturation)

        camera.set(cv2.CAP_PROP_AUTO_WB, self.auto_white_balance)
        camera.set(cv2.CAP_PROP_WB_TEMPERATURE, self.white_balance)

    def __str__(self):
        return f"{self.codec} @ {self.width}x{self.height} {self.fps}fps auto exposure: {self.auto_exposure} exposure: {self.exposure} saturation: {self.saturation}"


# Camera configurations
OV9782_CONFIG = CameraConfig(
    codec="MJPG",
    width=1920,
    height=1080,
    fps=100,
    auto_exposure=3,
    exposure=20,
    saturation=100,
    auto_white_balance=1,
    white_balance=0,
)


#class Camera(cv2.VideoCapture):
#    """
#    A wrapper for a generic camera using OpenCV's VideoCapture.
#
#    This class initializes a camera, applies the provided configuration, and provides utilities
#    to retrieve frames and properties like width and height.
#    """
#
#    def __init__(self, config: CameraConfig, port: int = 4):
#        super().__init__(port)
#
#        config.applyConfig(self)
#
#        print(f"Setup camera on port {port} with following settings: {config}")
#        print(f"Actual width x height: {self.width} x {self.height}")
#        print(f"Actual fps {self.get(cv2.CAP_PROP_FPS)}")
#        print()
#
#    @profile
#    def getFrame(self):
#        self.grab()
#        return self.retrieve()[1]
#
#    @property
#    def width(self):
#        return int(self.get(cv2.CAP_PROP_FRAME_WIDTH))
#
#    @property
#    def height(self):
#        return int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))

import cv2
from line_profiler import profile
import numpy as np

class RealsenseCamera:
    """
    Realsense-like camera using OpenCV VideoCapture for RGB + depth.
    Depth is an 8-bit approximation; real distances require pyrealsense2.
    """

    def __init__(self, rgb_port=4, depth_port=2, max_depth_mm=10000):
        """
        Initialize RGB and depth streams.

        :param rgb_port: OpenCV index for RGB camera
        :param depth_port: OpenCV index for depth camera
        :param max_depth_mm: Maximum depth distance for scaling 8-bit depth
        """
        self.rgb_cap = cv2.VideoCapture(int(rgb_port), cv2.CAP_V4L2)
        self.depth_cap = cv2.VideoCapture(int(depth_port), cv2.CAP_V4L2)
        self.max_depth_mm = max_depth_mm

        if not self.rgb_cap.isOpened():
            raise RuntimeError(f"Failed to open RGB camera on port {rgb_port}")
        if not self.depth_cap.isOpened():
            raise RuntimeError(f"Failed to open Depth camera on port {depth_port}")

        print(f"RealsenseCamera initialized. RGB port: {rgb_port}, Depth port: {depth_port}")

    @profile
    def getFrame(self):
        """
        Return RGB frame only (like old Camera interface).
        """
        ret_rgb, rgb = self.rgb_cap.read()
        if not ret_rgb:
            return None
        return rgb

    def getRGBDFrame(self):
        """
        Return a tuple (rgb_frame, depth_frame).
        Depth frame is 8-bit grayscale approximation.
        """
        ret_rgb, rgb = self.rgb_cap.read()
        ret_depth, depth = self.depth_cap.read()
        if not ret_rgb or not ret_depth:
            return None, None
        return rgb, depth

    def getDistanceAt(self, x, y, depth_frame=None):
        """
        Return approximate distance (in mm) at pixel (x, y).
        If depth_frame is not provided, reads a new depth frame.

        :param x: pixel column
        :param y: pixel row
        :param depth_frame: optional 8-bit depth frame
        :return: distance in mm (float)
        """
        if depth_frame is None:
            _, depth_frame = self.getRGBDFrame()
            if depth_frame is None:
                return None

        h, w = depth_frame.shape[:2]
        x = np.clip(x, 0, w - 1)
        y = np.clip(y, 0, h - 1)
        pixel_value = depth_frame[y, x]  # 0-255
        distance_mm = (pixel_value / 255.0) * self.max_depth_mm
        return distance_mm

    @property
    def width(self):
        return int(self.rgb_cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        return int(self.rgb_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
