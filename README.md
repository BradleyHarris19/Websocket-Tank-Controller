# Websocket-Tank-Controller
A way to control your rc tank from any browser on the network
## Outline
Following my limited sucess With the esp-32. I decided to take a different approach, using a Firmata Protocol client called pymata express to use ann arduino as a slave device to a wifi capable machine that runs the python and serves the webpage. I run it in docker as I am hoping to move my tank control to ROS2.
## Hardware
Originaly I used a Raspberry pi with an arduino nano, but I've moved it to a Jetson Nano and dockerised it. I use apache to serve the webpage. The arduino is connected to two LED's and a L298N Motor driver, with each tread of the tank connected to a motor.
