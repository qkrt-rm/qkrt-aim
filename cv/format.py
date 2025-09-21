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

"""
Runs a formatter on the src directory.
It makes code look pretty!
"""
import subprocess

LINE_LENGTH = 110

def main():
    # Run the black formatter on the src directory
    black_command = f"black src --line-length {LINE_LENGTH}"
    subprocess.run(black_command, shell=True, check=True)

    # Run the isort formatter on the src directory
    isort_command = f"isort src"
    subprocess.run(isort_command, shell=True, check=True)

if __name__ == "__main__":
    main()

