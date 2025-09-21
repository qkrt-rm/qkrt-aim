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
import subprocess
import os
from line_profiler import load_stats, show_text
import datetime

"""
Simple script to run the profiler and generate a log file.
Change python to whichever version you are using.
"""

def run_profiler():
    # Change directory to src
    os.chdir("src")

    # Run the profiler
    subprocess.run(["python", "-m", "kernprof", "-lvr", "main.py"])
    
    stats = load_stats("main.py.lprof")
    
    # Make timestamped file
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"profiler_output_{time}.txt"
    
    # Export this into a text file
    with open(file_name, "w") as f:
        show_text(stats.timings, unit=1e-7, rich=False, output_unit=1e-6, stream=f)
    
    # Change directory back to root
    os.chdir("..")
    
run_profiler()
