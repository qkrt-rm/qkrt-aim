Some of the dependencies have weird installation processes for Jetsons. Here's links to where you can find them

## First, install python
The version we install here is limited by our dependencies, our limiting 
factor being the version of ONNX Runtime we can support. At the time of writing,
that is python 3.12 and onnxruntime 1.19.0.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.12 python3.12-dev
```

## Next, install pip
After installing Python 3.12, you’ll need to ensure that pip is installed. Use the following commands:
```bash
sudo apt-get install python3.12-distutils-extra
wget https://bootstrap.pypa.io/get-pip.py | python3.12
python3.12 get-pip.py
```
If python3.12-distutils-extra doesn't work, you might need to change it to be python3.12-distutils.

Optionally, if you wish to use a virtual environment, you can install venv with the following command:
```bash
sudo apt-get install python3.12-venv
```

## Now to move on to our dependencies

## ONNX Runtime:
https://elinux.org/Jetson_Zoo#ONNX_Runtime
Go to this link and download the appropriate wheel file for your Jetson.
Simply click on the link and download the wheel file. Then, install it with pip:
```bash
pip install onnxruntime_gpu-1.19.0-cp312-cp312-linux_aarch64.whl
```
Replacing the name of the wheel file with the one you downloaded.


## Everything else:
From here, you can install the rest of the dependencies from our requirements.txt file:
```bash
pip install -r requirements.txt
```

## Running the application:
From here, you should be able to run the application with the following command:
```bash
cd src
python3.12 main.py
```

## Note about NumPy:
Depending on which version of onnxruntime you installed, you may need to install a specific version of numpy.
If you get an error saying that numpy is using a module built with version 1 of numpy and you have version 2 installed,
simply `pip install` the version of numpy specified. At the time of writing, this is 1.26.4, but pip may 
tell you the exact version you need to install. 

## GCC issues
If you get an issue saying:
ImportError: /lib/aarch64-linux-gnu/libstdc++.so.6: version `GLIBCXX_3.4.29' not found
Follow the instructions found in this post:
https://stackoverflow.com/questions/65349875/where-can-i-find-glibcxx-3-4-29


