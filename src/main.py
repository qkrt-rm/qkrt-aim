"""
This file is part of HuskyBot CV.
Copyright (C) 2025 Advanced Robotics at the University of Washington <robomstr@uw.edu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import cv2
from line_profiler import profile

from camera.Camera import OV9782_CONFIG, RealsenseCamera
from communication import RobotPositionMessage, Serial
from detector import HUSTDetector
from pose_estimator.TargetPositionEstimator import TargetPositionEstimator
from rules import CenterTargetRule, TargetSelector
from util import FrameRateTracker, Point3D, putTextOnImage

# Enable additional print info (slows loop; disable in deployment)
DEBUG = True

# Initialize components
detector = HUSTDetector("detector/models/HUST_model.onnx")
camera = RealsenseCamera(rgb_port=4, depth_port=2, max_depth_mm=10000)
pose_estimator = TargetPositionEstimator("example_camera_calibration.json")
target_selector = TargetSelector([CenterTargetRule(camera.width, camera.height)])
serial = Serial("/dev/ttyTHS1", 115200)

if DEBUG:
    tracker = FrameRateTracker(1.0)


def sendRobotPosition(position: Point3D):
    message = RobotPositionMessage(position)
    serial.write(message.createMessage())


@profile
def main():
    while True:
        # Get RGB + depth frames
        rgb_frame, depth_frame = camera.getRGBDFrame()
        if rgb_frame is None:
            continue

        frame = rgb_frame  # frame used for detection and display
        targets = detector.processInput(frame)
        has_any_target = len(targets) > 0

        # Estimate pose and send robot position
        if has_any_target:
            best_target = target_selector.getBestTarget(targets)
            _, target_rotation, target_position = pose_estimator.estimatePosition(best_target)
            sendRobotPosition(target_position)

        # Debug display & info
        if DEBUG:
            tracker.update()

            if has_any_target:
                print("Found targets:")
                for target in targets:
                    print(target)
                print("Best target:", best_target)
                print("Target position:", target_position)

            # Show approximate distance at center
            if depth_frame is not None:
                h, w = depth_frame.shape[:2]
                center_distance_mm = camera.getDistanceAt(w//2, h//2, depth_frame)
                cv2.putText(frame, f"Center Distance: {center_distance_mm} mm",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

            # Draw targets
            frame = putTextOnImage(frame, targets)

            # Display frame
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # Cleanup
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
