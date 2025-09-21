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

from math import sqrt

from detector import Target

from .SelectionRule import SelectionRule


class CenterTargetRule(SelectionRule):
    """
    An example rule that scores targets based on how close they are to the center of the image.
    Targets in the center of the image will have a score of 0, while targets further away will have a higher score.
    """

    def __init__(self, imageWidth: int, imageHeight: int):
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight

    def getScore(self, target: Target) -> float:
        # Get center of target
        center = target.getCenter()

        center.x = center.x / self.imageWidth
        center.y = center.y / self.imageHeight

        center.x = center.x - 0.5
        center.y = center.y - 0.5

        # Calculate the distance from the center
        return sqrt(center.x**2 + center.y**2)
