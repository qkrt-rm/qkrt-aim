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


@dataclass
class Point2D:
    x: float
    y: float

    def getMagnitude(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


@dataclass
class Point3D:
    x: float
    y: float
    z: float

    @staticmethod
    def convertFromOpenCVToNormalAxes(point: "Point3D") -> "Point3D":
        """
        OpenCV uses the axes coordinate system of:
            x positive: right
            y positive: down
            z positive: forwards away from camera

        Converts the axes to:
            x positive: forwards away from camera
            y positive: left
            z positive: up
        """
        return Point3D(point.z, -point.x, -point.y)

    def getMagnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5


class Rectangle:

    def __init__(self, bottomLeft: Point2D, topLeft: Point2D, topRight: Point2D, bottomRight: Point2D):
        self.bottomLeft = bottomLeft
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomRight = bottomRight

    def getCenter(self) -> Point2D:
        return Point2D((self.bottomLeft.x + self.topRight.x) / 2, (self.bottomLeft.y + self.topRight.y) / 2)

    def intersects(self, other) -> bool:
        return not (
            self.topRight.x <= other.bottomLeft.x
            or self.topRight.y <= other.bottomLeft.y
            or self.bottomLeft.x >= other.topRight.x
            or self.bottomLeft.y >= other.topRight.y
        )

    @property
    def vertices(self):
        return [self.bottomLeft, self.topLeft, self.topRight, self.bottomRight]


if __name__ == "__main__":
    point = Point2D(1, 2)
    print(point)

    rect = Rectangle(Point2D(0, 0), Point2D(0, 2), Point2D(2, 2), Point2D(2, 0))
    print(rect.getCenter())

    def testRectangle(bottomLeft1, topRight1, bottomLeft2, topRight2):
        rect1 = Rectangle(
            Point2D(*bottomLeft1),
            Point2D(bottomLeft1[0], topRight1[1]),
            Point2D(topRight1[0], topRight1[1]),
            Point2D(topRight1[0], bottomLeft1[1]),
        )
        rect2 = Rectangle(
            Point2D(*bottomLeft2),
            Point2D(bottomLeft2[0], topRight2[1]),
            Point2D(topRight2[0], topRight2[1]),
            Point2D(topRight2[0], bottomLeft2[1]),
        )
        print(rect1.intersects(rect2))

    testRectangle([0, 0], [2, 2], [1, 1], [3, 3])  # True
    testRectangle([0, 0], [1, 1], [1, 0], [2, 1])  # False
    testRectangle([0, 0], [1, 1], [2, 2], [3, 3])  # False

    import time

    start = time.perf_counter()
    for _ in range(1000):
        rect = Rectangle(Point2D(0, 0), Point2D(0, 2), Point2D(2, 2), Point2D(2, 0))
    end = time.perf_counter()
    print(f"Time elapsed: {end - start}")
