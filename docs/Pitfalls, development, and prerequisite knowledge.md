As a background to this section, this is from the perspective of someone who's primary done controls work in c++, with only
mild python experience using it for class projects. This was through exposure to ROS and some python work for ML projects.

# Prerequisite Knowledge

### If you plan on using and developing upon this repository, there are a few things you should know:
- Python syntax and basic programming concepts
  - Things like loops, conditionals, functions, classes, etc.
  - Object oriented programming concepts (classes, inheritance, etc.)
- Using a terminal
  - How to navigate directories
  - How to run python scripts
  - Using `sudo` to run scripts as root/admin
  - Being able to `pip install` packages
- A high-level understanding of how a computer works
    - What a CPU, GPU, RAM, and storage are
    - How data is stored and processed
    - What is an OS
    - What is USB and other ports
- Knowledge of how to use a version control system like git
    - How to clone a repository
    - How to commit and push changes
    - How to create and merge branches

### Knowledge that isn't required but is helpful:
- Knowledge of OpenCV
    - How to read and write images
    - How to do basic image processing and manipulation
    - What does it mean to calibrate a camera
- If you're pursuing better ML performance, knowledge of:
    - What is a neural network and what does it mean to inference
    - What is CUDA, and by extension, TensorRT

# Pitfalls

## Imports are weird

Python imports are weird. They're not like C++ where you can just include a header file and you're good to go. Instead, you have to
import the module you want to use. This can be done in a few ways:

1. Import the entire module
```python
import numpy
```
This imports the entire numpy module. To use a function from numpy, you would have to call it like this:
```python
numpy.array([1,2,3])
```

2. Import a specific function from a module
```python
from numpy import array
```

This imports the `array` function from the numpy module. To use it, you can call it directly:
```python
array([1,2,3])
```

3. Import a module with an alias
```python
import numpy as np
```

This imports the numpy module with the alias `np`. To use a function from numpy, you would call it like this:
```python
np.array([1,2,3])
```

Where I found this gets complicated is trying to import relative classes or functions from other files in the project. This is
done by using the `from` keyword. For example, to import the `TargetPositionEstimator` class from the `TargetPositionEstimator.py` file,
you would do:
```python
from TargetPositionEstimator import TargetPositionEstimator
```
This imports the specific class from the file instead of referencing the file itself. In the scenario where you have a file structure like this:
```plaintext
.
├── main.py
└── utils
    └── TargetPositionEstimator.py
```
You would have to do:
```python
from utils.TargetPositionEstimator import TargetPositionEstimator
```
Where this gets tedious is when you have several files in the same folder and trying to implement several of them. Instead here, we can introduce a `__init__.py` file in the `utils` folder. This file is used to tell python that the folder is a package and can be imported as such. This allows us to do:
```python
from utils import TargetPositionEstimator
```
and if we had extra files in the `utils` folder, we could import them in the same way:
```python
from utils import TargetPositionEstimator, OtherClass1, OtherClass2, ...
```


