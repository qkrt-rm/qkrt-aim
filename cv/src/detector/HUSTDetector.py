from typing import List

import cv2
import numpy as np
from cv2.typing import MatLike

from util import Point2D

from .Detector import Detector
from .Target import Target, mergeListOfTargets


class HUSTDetector(Detector):
    """
    Ok this class is a bit complicated, comments are based off of the original code.
    It's an implementation of the detector from HUST's 2023 HERO open source.
    The logic is based off of this code:
    https://github.com/HUSTLYRM/HUST_HeroAim_2024/blob/main/src/armor_detector/src/Inference.cpp
    """

    INPUT_SIZE = 416
    BOUNDING_BOX_CONFIDENCE_THRESHOLD = 0.85

    color_to_word = ["Blue", "Red", "Neutral", "Purple"]
    tag_to_word = ["Sentry", "1", "2", "3", "4", "5", "Outpost", "Base"]

    def __init__(self, model_path: str) -> None:
        super().__init__(model_path)
        self.offsets = self.generateOffsets()

        # Warmup the model to build/cache anything needed for processing
        input_shape = (1, 3, self.INPUT_SIZE, self.INPUT_SIZE)
        dummy_input = np.zeros(input_shape, dtype=np.float32)
        self.model.run(None, {"images": dummy_input})

    def processInput(self, input: MatLike) -> List[Target]:
        input, scalar_h, scalar_w, x_cutoff = self.formatInput(input)

        output = self.model.run(None, {"images": input})
        output = np.array(output)[0][0]

        targets: List[Target] = self.getTargetsFromOutput(output)

        # Scale the targets back to the original image size
        for target in targets:
            vertices = target.rect.vertices
            for i in range(4):
                vertices[i].x = vertices[i].x * scalar_w + x_cutoff
                vertices[i].y = vertices[i].y * scalar_h

        targets = mergeListOfTargets(targets)

        return targets

    # Format input to target expected model input of (1, 3, 416, 416)
    def formatInput(self, img: MatLike):
        # Chop off the sides to make it square
        x_cutoff = 0
        if img.shape[1] != img.shape[0]:
            x_cutoff = img.shape[1] - img.shape[0]
            x_cutoff = x_cutoff // 2
            img = img[:, x_cutoff : x_cutoff + img.shape[0]]

        # Resize the image to the input size of the model
        scalar_h = img.shape[0] / self.INPUT_SIZE
        scalar_w = img.shape[1] / self.INPUT_SIZE

        # Image shape is resized to (416, 416, 3)
        img = cv2.resize(img, (self.INPUT_SIZE, self.INPUT_SIZE))

        # Model input expects (1, 3, 416, 416), conversion to NCHW
        img = img.transpose((2, 0, 1))
        img = np.expand_dims(img, axis=0)

        # Convert to float32
        img = img.astype(np.float32)

        return img, scalar_h, scalar_w, x_cutoff

    def getTargetsFromOutput(self, values) -> List[Target]:
        targets = []

        NUM_COLORS = 8
        NUM_TAGS = 8

        # Look only at the rows that have high confidence
        indices = np.where(values[:, 8] > self.BOUNDING_BOX_CONFIDENCE_THRESHOLD)
        values = values[indices]

        currOffsets = self.offsets[indices]

        # Go through each row and create a target
        for element, offset in zip(values, currOffsets):
            x_offset, y_offset, scalar = offset[0], offset[1], offset[2]

            x_1 = (element[0] + x_offset) * scalar
            y_1 = (element[1] + y_offset) * scalar
            x_2 = (element[2] + x_offset) * scalar
            y_2 = (element[3] + y_offset) * scalar
            x_3 = (element[4] + x_offset) * scalar
            y_3 = (element[5] + y_offset) * scalar
            x_4 = (element[6] + x_offset) * scalar
            y_4 = (element[7] + y_offset) * scalar

            confidence = element[8]

            color = np.argmax(element[9 : 9 + NUM_COLORS])
            tag = np.argmax(element[9 + NUM_COLORS : 9 + NUM_COLORS + NUM_TAGS])

            bottomLeft = Point2D(x_1, y_1)
            topLeft = Point2D(x_2, y_2)
            topRight = Point2D(x_3, y_3)
            bottomRight = Point2D(x_4, y_4)

            target = Target(
                [bottomLeft, topLeft, topRight, bottomRight],
                self.color_to_word[int(color / 2)],
                self.tag_to_word[tag],
                confidence,
            )
            targets.append(target)

        # Sort the targets by confidence
        targets.sort(reverse=True)

        return targets

    def generateOffsets(self):
        STRIDES = [8, 16, 32]
        output = []
        for scalar in STRIDES:
            grid_h = self.INPUT_SIZE // scalar
            grid_w = self.INPUT_SIZE // scalar
            for y in range(grid_h):
                for x in range(grid_w):
                    output.append((x, y, scalar))
        output = np.array(output)
        return output
