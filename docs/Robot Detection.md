# Chat, what's CV?

CV, or computer vision, is the process of teaching a computer to "see". It involves taking in an image, processing it,
and getting useful information in return. For RoboMaster specific guidance and information, the best resource is Kaelin's
guide on the RoboMaster NA forums: https://forums.robomasterna.com/t/so-you-want-to-build-an-auto-aim-system-the-dramatically-overstated-definitive-guide-to-shooting-things-good/160

The short version? We're creating a system that takes in an image and tells us where the robots are. To do this, 
we are using a neural network—a bit of code that takes in an input (an image in our case), process it through layers of math,
and outputs something useful (the location of the robots). The specific math being done through the layers and how much each
layer affects the final output is known as a model.

## How do we run it?

To run a model, we rely on libraries designed to simplify neural network execution. Popular ones include TensorFlow and PyTorch.
In our case, the model is saved in the .onnx format, based on Microsoft’s ONNX (Open Neural Network Exchange) standard. We use Microsoft’s
ONNXRuntime library to run the model.

Here's the general process:  
Step 1) Load in the model  
In the code, it's `model = onnxruntime.InferenceSession(model path)`

Step 2) Run the model  
In the code, it's `output = model.run(model input)`  

ONNXRuntime makes running models straightforward. But here’s the catch: running the model like this defaults to using your CPU.
While CPUs are great for a lot of things, they're not the best at doing a lot of math quickly. On a Jetson Nano, it takes around
35ms per frame, giving you about 30 frames per second (fps). This is fine for many applications, but for the fast paced engagements in
RoboMasters, we need better.

## How do we make it faster?

Behold, the GPU! Unlike CPUs, GPUs are optimized for doing math quickly. They do this by having many cores and paralleling the math.
To make use of the GPU on the jetson, Nvidia provides a library called CUDA. With CUDA, you can tell ONNXRuntime to run the model on the GPU instead of the CPU.
Here’s how:

`model = onnxruntime.InferenceSession(model_path,providers=['CUDAExecutionProvider'])`

Utilizing the GPU massively speeds up the model. Instead of 35ms per frame, it now takes 10ms to run the model.
This bumps up our frame rate to a theoretical 100 fps. For more information on CUDA and the other various 
execution providers, check out the ONNXRuntime documentation: https://onnxruntime.ai/docs/execution-providers/


## But can we do better?

Indeed! Behold, TensorRT! TensorRT is another library made by Nvidia specifically designed to run neural networks on their GPUs.
It takes in the model and performs a series of optimizations to make in run even faster, removing unnecessary computations and folding in 
several operations into one. Using TensorRT is as simple as adding in CUDA, we simply need to specify that we want to use it:  

`model = onnxruntime.InferenceSession(model path, providers=['TensorRTExecutionProvider'])`

The result: insanely fast runtimes. Running the model now takes around 3.5ms per frame, achieving a theoretical framerate of 300fps.
Poggers!


## TensorRT tips

To get the most out of TensorRT, we can specify a few settings:

Caching the engine:
Converting a model to a TensorRT engine can take a while—sometimes minutes. To avoid doing this every time, you can save the engine
to a file and reuse it later. This allows us to get the vision system up and running quicker.

Precision:
By default, models use 32-bit floating-point precision. This is accurate, but slow. TensorRT can convert the model to 8-bit integer precision
(INT8), trading a slight drop in accuracy for around a 40% speed boost. Using INT8, our model runs in ~1.8ms, pushing us over 500 fps while detecting
robots as far away as 6m! These benchmarks are with using TensorRT directly, ONNXRuntime on the other end has some overhead that can slow it down
and requires a few more inputs to make INT8 work. As such, we have instead enabled FP16 precision by default. 
