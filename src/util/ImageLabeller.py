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

import cv2

from detector import Target


def putTextOnImage(img, boxes: List[Target]):
    """
    Utility function to draw bounding boxes around detected targets in an image.
    Displays the tag, color, and confidence of the target above the bounding box.
    """

    for i in range(len(boxes)):
        box = boxes[i]
        for j in range(4):
            cv2.line(
                img,
                (int(box.rect.vertices[j].x), int(box.rect.vertices[j].y)),
                (int(box.rect.vertices[(j + 1) % 4].x), int(box.rect.vertices[(j + 1) % 4].y)),
                (0, 255, 0),
                2,
            )

        # Put first letter of color capitalized, tag, and then confidence (rounded to 2 decimal places)
        label = f"{box.color[0].upper()} {box.tag} {box.confidence:.2f}"

        cv2.putText(
            img,
            label,
            (int(box.rect.vertices[0].x), int(box.rect.vertices[0].y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    return img
