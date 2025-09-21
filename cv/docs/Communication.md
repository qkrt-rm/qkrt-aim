# Communication
We are using the DJI Referee System Serial Protocol to send our messages back to the MCB. 
This is done as Taproot already has a parser built in for these types of messages.

The exact specification for this protocol can be found here:
https://terra-1-g.djicdn.com/b2a076471c6c4b72b574a977334d3e05/RM2024/RoboMaster%20Referee%20System%20Serial%20Port%20Protocol%20Appendix%20V1.6.1%EF%BC%8820240126%EF%BC%89.pdf

## Implementation notes

You might notice that when creating the serial object, you have to specify the port and the baudrate.
While the port is fairly self explanatory, the baudrate might not be. The baudrate is the speed at which we are 
sending the data over the port. The higher the baudrate, the more bits per second we attempt to send. While it might sound
tempting to set the baudrate to the highest possible value, it is important to note that the higher the baudrate, the more
likely it is that the data will get corrupted during transmission. As such, we have to find a balance between speed and reliability.
In our case, 1 megabaud, or 1 million bits per second. We've chosen this as in our testing, it has been the fastest baudrate 
that works reliably for us. If you are planning on sending this information through a slip ring, you may need to lower the baudrate.
ARUW tends to use 0.5 megabaud, or 500,000 bits per second, when dealing with slip rings.

## Perms for serial
When you first try to run the code, you may get a permission error for opening the port '/dev/ttyTHS0'.
To fix this, try running the following commands:
```bash
sudo usermod -a -G dialout $USER
sudo systemctl stop nvgetty.service
sudo systemctl disable nvgetty.service
```

If that doesn't work, try this:
```bash
sudo chmod 666 [PORT]
```
where `[PORT]` is the port you are trying to open. This is of format of `/dev/ttyTHS0`.
