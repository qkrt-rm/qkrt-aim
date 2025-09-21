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

from abc import ABC, abstractmethod
from typing import List

import onnxruntime as ort

from .Target import Target


class Detector(ABC):
    """
    Abstract base class for an image detector. This class takes in an image and returns a list of targets found in the image.

    Note:
    This is using the ONNXRuntime library, which is a library used to load and run ONNX models.
    ONNX is an open source standard for storing machine learning models. We use this library to run inference on the image to find targets.
    Alternative libraries are TensorFlow and PyTorch.
    """

    def __init__(self, model_path: str):
        super().__init__()
        self.model = ort.InferenceSession(model_path, providers=self.configureProviders())

    @abstractmethod
    def processInput(self, input) -> List[Target]:
        pass

    def configureProviders(self):
        """
        ONNXRuntime uses "Execution Providers" to specify settings for the different platforms that can be used to run the model.
        Here, we first give priority to TensorRT, then CUDA, and if neither of these are available, we fall back to using the CPU.
        """
        return [
            (
                "TensorrtExecutionProvider",
                {
                    # Set GPU memory usage limit, this is in bytes (2**30 = 1GB)
                    "trt_max_workspace_size": (2**30),
                    # Enable FP16 precision for faster inferencing
                    "trt_fp16_enable": True,
                    # Cache created engine so it doesn't have to be recreated every time
                    "trt_engine_cache_enable": True,
                    # Directory to store the cached engine
                    "trt_engine_cache_path": "./detector/models/trt_engines",
                },
            ),
            ("CUDAExecutionProvider"),
            ("CPUExecutionProvider"),
        ]
