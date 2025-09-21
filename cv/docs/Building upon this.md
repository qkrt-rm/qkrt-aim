# Where to go from here?

Now that you have a basic understanding of how the vision system works, you can start building upon it. Here are a few ideas to get you started:

## Persistence

Due to the nature of the model, it doesn’t detect the armor plate in every image perfectly. In a sequence of images, it’s common for a few frames
to not result in any detection. However, we know that if we just saw a target, it’s very likely that the target is still there in the next frame.
Knowing where a plate previously was and being able to correlate it with a new plate allows you to unlock a lot of future development capabilities

## Tracking robots

Something that becomes evident pretty early on is that while aiming at a immobile or slow moving target seems to track well, tracking a fast moving
target becomes difficult. This is because we are only returning the position of the plate and not the velocity it’s moving at. How can we compute the
velocity the plate is moving at so we can better predict? A handy bit of physics tells us that velocity is just the difference between the current
position and the previous position, perhaps we can use those persistence features we just mentioned? 

## More FOV

Currently the HUST model expects a fixed square input size. My solution is to take a center crop of the image, losing horizontal FOV. Are there better
ways of analyzing the full image? Avenues to explore may be padding the top and bottom of the image to make it square, which can come at the cost of loss
of resolution after resizing, or perhaps running the model several times on segmented parts of the image, at the cost of added runtime.

## Localization

Once you figured out how to track an enemy robot, you may quickly come to the new problem: all the motion is relative to your camera, if you start moving,
it shows up as movement in the enemy plate. Your velocity will start reflecting both your own movement as well as the enemy robot’s movement, which can
lead to increased noise and worse accuracy. If only there was a way to know the speed at which we were moving and account for that when computing the enemy
robot position and velocity?

## Noise reduction
Once you start tracking the position and staring at an image for a while, you might start to notice that “hey, this bounding box is shifting around a lot and creating weird noise”.
Those slight movements get noticed as velocity and can make your turret shake trying to follow constantly shifting setpoints. Once you start logging the position, you might want
to check it against a histogram and notice that a lot of your measurements seemed to be centered around a point and make…a gaussian distribution? Behold the world of sensors and
measurement noise, where people have spent decades trying to remove noise from measurements. There’s a plethora of ways to cut out noise from low-pass, moving average, Kalman Filters,
Particle Filters, and many more! My personal favorite python library to do this with is FilterPy, it’s quite fast, has plenty of filters available, and is easy to use.

## 3v3: More targets, more selection rules, more logic!
Once you get to 3v3, a lot of new possibilities open up! There’s potentially going to be > 1 robot in frame, how do you keep track of which robot is which? How do you keep track of
which robot to aim at? Aiming at the center of the image is fine, but what if that robot was 10m away and there was another 2m away? What if we wanted to shoot the robot that has less HP?
What if we wanted to ignore robots that were immune?

## Make a better model

The HUST model is a great starting point, but it’s not perfect. We don't know what dataset it was trained on, what architectural decisions were made, or what the training process was like.
As such, we can't improve upon the model. To go forward from here, you should consider training your own model. This can be done by collecting a dataset of images and labelling them with
items of interest. Once you have a dataset, you can train a model using tools like PyTorch or TensorFlow. This will allow you to have a model that is tailored to your specific needs.

## Fiducial Markers

Fiducial markers, like AruCo markers or AprilTags, are a great way to do localization, as it allows you to localize yourselves on the map. This can be used to improve the accuracy of the
robot tracking as well as allow you to do more advanced tasks like path planning. Fiducial marker detection is fairly easy to use, OpenCV has built in support for this. The OV9782 camera 
module was selected for it's global shutter capability, which is useful for reducing blur in fiducial marker detection. For further resources, try looking into the FRC and FTC space
as they have been using AprilTags for the last few years and have several well made guides about detection and tuning.


