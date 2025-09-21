# Tuning the system

There's currently a few items in this repository that require per system tuning.

## Camera calibration

Each camera has unique distortion and focal length parameters, which effect the accuracy of positional estimation.
To tune the camera calibration, there's tuning guides from [https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html](OpenCV),
[https://www.calibdb.net/](CalibDB), and [https://mrcal.secretsauce.net/](mrcal) which can be used to generate a calibration file.

## Target Position Estimation

Since we don't utilize a depth or stereoscopic cameras in this repository, we do target position estimation based on the size of the target in the image.
This requires tuning of the `PLATE_HEIGHT_M` in `TargetPositionEstimator.py` to match the actual position of the target in real life. The easiest way to do this is to place
an armor plate at a known distance from the camera and adjust the `PLATE_HEIGHT_M` until the estimated position matches the actual position. For best accuracy,
tune this parameter to where you plan on taking most engagements from, for a 1v1 field that's likely in the 1-2m range. 

## Serial Communication
Please refer to the `Communication.md` file to see suggestions for baudrates.
