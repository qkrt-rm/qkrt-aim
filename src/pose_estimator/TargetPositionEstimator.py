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

import json

import cv2
import numpy as np

from detector import Target
from util import Point3D


class TargetPositionEstimator:
    """
    This class attempts to compute the position of the target in 3D space. It does this by using the camera calibration
    giving us values like the FOV, focal length, and distortion. Using these values and the position of the target within
    the image, we can estimate the position and rotation of the target in 3D space.

    Documentation regarding how this works can be found at:
    https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html
    """

    def __init__(self, camera_calibration_file: str):
        with open(camera_calibration_file) as f:
            camera_calibration = json.load(f)

            self.camera_matrix = np.array(camera_calibration["camera_matrix"]["data"]).reshape(3, 3)

            self.distortion_coefficients = np.array(
                camera_calibration["distortion_coefficients"]["data"]
            ).reshape(5, 1)

        print("Created TargetPositionEstimator with camera calibration: ")
        print("Camera matrix: ", self.camera_matrix)
        print("Distortion coefficients: ", self.distortion_coefficients)
        print()

        self.PLATE_WIDTH_M = 0.135
        # Since the model puts a bounding around the light bar, this height is the height of the LEDs
        self.PLATE_HEIGHT_M = 0.055

        self.object_points = np.array(
            [
                (0, 0, 0),
                (0, self.PLATE_HEIGHT_M, 0),
                (self.PLATE_WIDTH_M, self.PLATE_HEIGHT_M, 0),
                (self.PLATE_WIDTH_M, 0, 0),
            ]
        ).astype(np.float32)

        self.aspect_ratio = self.PLATE_WIDTH_M / self.PLATE_HEIGHT_M

    def estimatePosition(self, detected_target: Target):
        """
        Estimates the position of the target in camera space

        args:
            detected_target: The target detected in the image

        returns:
            success: True if the estimation was successful
            rotation_vector: The rotation of the target in camera space
            translation_vector: The translation of the target in camera space
        """
        detected_target = self.fixAspectRatio(detected_target)

        # Convert the vertices of the bounding box to a numpy array
        points = detected_target.rect.vertices
        image_points = np.array(
            [
                [points[0].x, points[0].y],
                [points[1].x, points[1].y],
                [points[2].x, points[2].y],
                [points[3].x, points[3].y],
            ]
        ).astype(np.float32)

        # Compute the position of the target in 3D space
        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.object_points,
            image_points,
            self.camera_matrix,
            self.distortion_coefficients,
        )

        translation_vector = Point3D(*translation_vector.flatten())
        translation_vector = Point3D.convertFromOpenCVToNormalAxes(translation_vector)

        return success, rotation_vector, translation_vector

    def fixAspectRatio(self, detected_target: Target) -> Target:
        """
        Changes the aspect ratio of the detection to make the width target the aspect ratio given height.
        This is done because as the target rotates, the bounding box around the target will change shape, leading
        to incorrect position estimation. As a solve, we attempt to fit the given bounding box to the expected dimensions
        of a plate.
        """
        target_height = detected_target.rect.topLeft.y - detected_target.rect.bottomLeft.y
        expected_width = target_height * self.aspect_ratio

        detected_target.rect.topRight.x = detected_target.rect.topLeft.x + expected_width
        detected_target.rect.bottomRight.x = detected_target.rect.bottomLeft.x + expected_width

        return detected_target
