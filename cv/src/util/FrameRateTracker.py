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

import time


class FrameRateTracker:
    """
    Utility class to keep track of the frame rate of a process.
    Counts updates per second and prints the number of updates processed per update_interval.
    """

    def __init__(self, update_interval_seconds=1.0):
        self.start_time = time.time()
        self.frame_count = 0
        self.update_interval = update_interval_seconds

    def update(self):
        self.frame_count += 1

        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.update_interval:
            print(f"Processed {self.frame_count} camera frames in the last {self.update_interval} second(s)")
            self.start_time = current_time
            self.frame_count = 0


if __name__ == "__main__":
    tracker = FrameRateTracker()

    while True:
        tracker.update()
