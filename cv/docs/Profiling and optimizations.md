# How to profile

We are using the python package `line profiler` to profile the code. This works by annotating a method with the `@profile` decorator.
From here, any method we want to profile can be setup with first importing in the `line_profiler` package and then annotating the method with `@profile`.
Example:
```python
from line_profiler import profile

@profile
def x():
    return 1
```

To run this profiler, we need to run the following command (replacing `python` with the installed version):
```bash
python -m kernprof -lvr <file>.py
```

This will generate a file holding all of our statistics, and by default uses a microsecond timer.

## Automation!

To automate running the script, and processing the output, please use the `profiler.py` file. This runs the profiling command on the `main.py` file, waits until exited, and then saves the output to a file. The output is then printed using the millisecond timer for easier reading. To use this well, either change the `main.py` file to end after a certain amount of time, or if using the DEBUG view,
end the program by hitting `q` on the camera feed. Please make sure to replace `python` with whatever installed version you have.

## Understanding the output

Let's look at the following profiler log:
```
Timer unit: 1e-06 s


Total time: 27.6878 s
File: main.py
Function: main at line 38

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    38                                           @profile
    39                                           def main():
    40       805       1109.0      1.4      0.0      while True:
    41       805   19169764.6  23813.4     69.2          frame = camera.getFrame()
    42       805    6374711.8   7918.9     23.0          targets = detector.processInput(frame)
```

The left most column is the line number in our code. The `Hits` column is the number of times that line was run. The `Time` column is the total time spent executing that line of code.
The `Per Hit` column is the average time spent on that line. The `% Time` column is the percentage of the total time spent on that line. The `Line Contents` column is the actual code that was executed.

So in the context of the line `targets = detector.processInput(frame)`, we can see that this line was run 805 times, and took 23.0% of the total loop time.
Each time it was run, it took on average 7918.9 microseconds to execute. From here, you can see where the majority of your loop time is being spent and can add additional `@profile` annotations to specific methods to get more info about them.


# Optimizations that can be made

## Threading

An optimization that can be made is to use threading to grab camera frames in the background while your main loop runs. This can be done by creating a new thread 
that runs the camera feed, and then the main thread can run the detector. This will allow the detector to run while the camera is grabbing frames, and
can help speed up the overall process. Be wary that python versions less than 3.13 implement "true" threading, and may not be as efficient as expected.
Look up "Python Global Interpreter Lock" for more information. 

## TensorRT

ONNXRuntime adds some extra overhead compared to running tensorRT directly. In our benchmarks, this is approximately 1-2ms slower with the HUST
detector model. Switching over to using TensorRT directly will help speed up the inference time, but this will require some extra work to implement.
To help make the engine model required to use TensorRT, try using the `trtexec` command to generate the engine file. This comes preinstalled on jetsons
that have TensorRT enabled via SDKManager.

## Gstreamer

GStreamer is a pipeline based framework that for our case, allows us to more efficiently read in frames from the camera. This is because GStreamer is used to decode
the camera input and convert it to a format that OpenCV can use all while the data is still in memory, not on the CPU. This allows us to significantly reduce the CPU load
as well as the time it takes to read in frames from the camera. 

To get started with GStreamer, either consider using OpenCV with GStreamer or use a different library, such as `PyGObject`. The version of CUDA that gets installed via pip
does not include GStreamer support by default, so you will need to build OpenCV from source with GStreamer support. NVidia developers have scripts that can help with this, 
which can be found [here](https://github.com/AastaNV/JEP/tree/master/script). An example of a pipeline that uses `PyGObject` can be found [here](https://github.com/TheImagingSource/tiscamera/blob/master/examples/python/07-appsink.py).

When going up to create a pipeline, you will need to describe the dataflow. As such, we will look at the following example string:
```bash
v4l2src device={DEVICE_PATH} ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGR ! appsink
```

Here, this is saying that we want to use `v4l2src` to read in data from the camera, which is a video handler for linux. From there, we want to use the `nvv4l2decoder` element to 
decode the data, NVidia's hardware accelerated decoder. After that, we want to use the `nvvidconv` element to convert the data to a format that OpenCV can use (BGR camera format). Finally, we
want to use the `appsink` element to send the data to OpenCV.

In our testing, we saw that converting in pipeline to BGR was slower than taking BGRx data and converting it in BGR ourselves. This can either be done using a converter such as OpenCV's `cv2.cvtColor` or by manipulating the numpy array directly to remove the alpha channel. With this, we saw that the time to read in frames was reduced to around 1.1 ms.
