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
camera = RealsenseCamera(rgb_port=4, depth_port=0, max_depth_mm=10000)
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

        if DEBUG:
            tracker.update()

            if has_any_target:
                print("Found targets:")
                for target in targets:
                    print(target)
                print("Best target:", best_target)
                print("Target position:", target_position)

            # Draw targets (in-place)
            putTextOnImage(frame, targets)

                        # Show RGB last
            cv2.imshow("Frame", frame)

            # Distance text
            if depth_frame is not None:
                # --- Convert depth to grayscale ---
                if len(depth_frame.shape) == 3:
                    depth_gray = cv2.cvtColor(depth_frame, cv2.COLOR_BGR2GRAY)
                else:
                    depth_gray = depth_frame.copy()

                # --- Normalize for display ---
                depth_vis = cv2.normalize(
                    depth_gray,
                    None,
                    0,
                    255,
                    cv2.NORM_MINMAX
                ).astype("uint8")

                h, w = depth_vis.shape
                cx, cy = w // 2, h // 2

                # --- Get distance at center ---
                center_distance_mm = camera.getDistanceAt(cx, cy, depth_gray)

                # --- Draw crosshair ---
                cv2.drawMarker(
                    depth_vis,
                    (cx, cy),
                    255,
                    markerType=cv2.MARKER_CROSS,
                    markerSize=20,
                    thickness=2
                )

                # --- Draw distance text ON DEPTH FRAME ---
                if center_distance_mm is not None:
                    cv2.putText(
                        depth_vis,
                        f"{float(center_distance_mm):.1f} mm",
                        (cx - 80, cy - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        255,
                        2
                    )

            
            cv2.imshow("Depth Frame", depth_vis)



            #cv2.imshow("Depth Frame", depth_gray)



            if cv2.waitKey(1) & 0xFF == ord("q"):
                break





    # Cleanup
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
