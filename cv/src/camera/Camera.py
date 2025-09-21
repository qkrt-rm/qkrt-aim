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
    width=1280,
    height=800,
    fps=100,
    auto_exposure=1,
    exposure=0,
    saturation=100,
    auto_white_balance=1,
    white_balance=0,
)


class Camera(cv2.VideoCapture):
    """
    A wrapper for a generic camera using OpenCV's VideoCapture.

    This class initializes a camera, applies the provided configuration, and provides utilities
    to retrieve frames and properties like width and height.
    """

    def __init__(self, config: CameraConfig, port: int = 0):
        super().__init__(port)

        config.applyConfig(self)

        print(f"Setup camera on port {port} with following settings: {config}")
        print(f"Actual width x height: {self.width} x {self.height}")
        print(f"Actual fps {self.get(cv2.CAP_PROP_FPS)}")
        print()

    @profile
    def getFrame(self):
        self.grab()
        return self.retrieve()[1]

    @property
    def width(self):
        return int(self.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        return int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))
