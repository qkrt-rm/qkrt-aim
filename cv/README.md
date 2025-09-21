# CV

A flexible Computer Vision (CV) system for the RoboMaster robotics competition.

This repository provides an MVP (minimum viable product) CV framework for teams just getting started with Computer Vision in the context of RoboMaster's 1v1 competition. It is designed as a robust and extensible starting point, offering an easy-to-understand foundation while enabling advanced teams to expand on its capabilities.

## Features

- Armor detection: Detects armor plates using HUST open source armor detector model
- Customizable target selection: Ideal aiming target is chosen through a system of rules to evaluate various detected plates
- Hardware Acceleration: Leverages Nvidia CUDA and TensorRT for accelerated inferencing on supported GPUs, optimizing performance.

## Recommended Hardware

This system is intended for deployment on a co-processor, optimized for devices with Nvidia GPU support. The recommended hardware is:

- **Nvidia Jetson Orin Nano Super:** Compact co-processor with GPU (similar to RTX3060 level of compute) and 
currently retails for $250. The value of this device far outweighs similarly priced competitor options, and even those at lower prices such 
as the Raspberry/Orange Pi devices. The Jetson Nano provides a higher compute ceiling, allowing teams to expand and develop more complex systems
before reaching the limitations of their hardware. 
  - **Recommended upgrade**:  Add an M.2 2280 NVMe SSD (PCIe 3.0x4) for increased storage capacity. Without this, storage is limited to microSD cards or on-board storage.

- **OV9782 Global Shutter Camera:** 1280x800 100FPS USB Camera. Global shutter results in less blur during heavy motion compared to rolling shutter modules.
Currently retails for $60.  


## Installation and Running
To get started with this system, follow the setup instructions in the `docs/Installation.md` file.


## Contributing
Contributions are welcome! If you have ideas to improve the system or encounter issues,
feel free to submit a pull request or open an issue in this repository.


## License
This project is licensed under the GPL-3.0 License - see the `LICENSE` file for details.


## Future plans for this repository

- [ ] Benchmark using Jetson Orin Nano Super. System is currently benchmarked using a Jetson AGX Xavier, which is constrained to jetpack 5.1.4.
As such, testing was done with python3.11, CUDA 11.4, and TensorRT 8.5. The Jetson Orin Nano Super is capable of running Jetpack 6, which boosts
all of these versions to the latest available
