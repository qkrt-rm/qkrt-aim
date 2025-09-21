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

import cv2
from line_profiler import profile

from camera.Camera import OV9782_CONFIG, Camera
from communication import RobotPositionMessage, Serial
from detector import HUSTDetector
from pose_estimator.TargetPositionEstimator import TargetPositionEstimator
from rules import CenterTargetRule, TargetSelector
from util import FrameRateTracker, Point3D, putTextOnImage

# Enable additional print info
# This does slow down main loop, do not enable in deployment
DEBUG = True

detector = HUSTDetector("detector/models/HUST_model.onnx")
camera = Camera(OV9782_CONFIG)
pose_estimator = TargetPositionEstimator("example_camera_calibration.json")
target_selector = TargetSelector([CenterTargetRule(camera.width, camera.height)])
serial = Serial("/dev/ttyTHS0", 1_000_000)

if DEBUG:
    tracker = FrameRateTracker(1.0)


def sendRobotPosition(position: Point3D):
    message = RobotPositionMessage(position)
    serial.write(message.createMessage())


@profile
def main():
    while True:
        frame = camera.getFrame()
        targets = detector.processInput(frame)

        has_any_target = len(targets) > 0

        if has_any_target:
            best_target = target_selector.getBestTarget(targets)
            _, target_rotation, target_position = pose_estimator.estimatePosition(best_target)
            sendRobotPosition(target_position)

        if DEBUG:
            tracker.update()

            if has_any_target:
                print("Found targets:")
                for target in targets:
                    print(target)
                print("Best target:", best_target)
                print("Target position:", target_position)

            frame = putTextOnImage(frame, targets)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
