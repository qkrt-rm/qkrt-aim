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

from typing import List

from util import Point2D, Rectangle


class Target:
    """
    Represent a detected target plate.

    args:
        points (List[Point2D]): A list of four points representing the corners of the target. In order of BL, TL, TR, BR.
        color (str): The color of the target.
        tag (str): A label or tag for the target.
        confidence (float): The confidence score of the detection (between 0 and 1).
    """

    def __init__(self, points: List[Point2D], color: str, tag: str, confidence: float):
        if len(points) != 4:
            raise ValueError("A Target must have exactly 4 points (to form a rectangle).")

        self.rect = Rectangle(*points)
        self.color = color
        self.tag = tag
        self.confidence = confidence

    def __str__(self):
        """
        Returns a formatted string representation of the target.
        Example: "Red Sentry, Confidence: 0.90, Points: (0,0) (0,1) (1,1) (1,0)"
        """
        # This line is a bit wacky, but it's just a fancy way to format the points
        points = "".join([f"({round(p.x, 2)}, {round(p.y, 2)}) " for p in self.rect.vertices])
        return f"{self.color} {self.tag}, Confidence: {self.confidence: .2f}, Points: {points}"

    def __lt__(self, other: "Target"):
        # Sort by confidence
        return self.confidence < other.confidence

    def getCenter(self) -> Point2D:
        return self.rect.getCenter()


def isOverlap(target1: Target, target2: Target) -> bool:
    # Check if the rectangles overlap
    return target1.rect.intersects(target2.rect)


def mergeTargets(target1: Target, target2: Target) -> Target:
    # If they are not same tag, throw an error
    # This is done to avoid merge two close-by plates
    if target1.tag != target2.tag:
        raise ValueError("Rectangles must have same color and tag to merge")

    # Return the rectangle with the highest confidence, perhaps something to improve upon in the future?
    return target1 if target1.confidence > target2.confidence else target2


def mergeListOfTargets(targets: List[Target]) -> List[Target]:
    """
    Merges a list of targets, combining overlapping targets with the same tag.
    """
    merged_targets: List[Target] = []
    for target in targets:
        for j in range(len(merged_targets)):
            # Merge the targets if they overlap
            if isOverlap(target, merged_targets[j]) and (target.tag == merged_targets[j].tag):
                merged_targets[j] = mergeTargets(target, merged_targets[j])
                break
        else:
            merged_targets.append(target)

    return merged_targets


if __name__ == "__main__":
    target1 = Target((Point2D(0, 0), Point2D(0, 1), Point2D(1, 1), Point2D(1, 0)), "Red", "Sentry", 0.9)
    print("First target:", target1)

    target2 = Target((Point2D(0, 0), Point2D(0, 1), Point2D(1, 1), Point2D(1, 0)), "Neutral", "Sentry", 0.95)
    print("Second target:", target2)

    merged = mergeListOfTargets([target1, target2])
    print("Merged targets:", merged)

    print("Center of first target:", target1.getCenter())
