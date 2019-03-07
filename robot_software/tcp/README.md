# Wireless BOB Guide

## TODO

Set up ZeroConf for TCP connection publishing

## WTF is this code

This folder is designed to take over from `mongo_client.py` and take the load of connecting to the server off the EV3 as well as giving us more ports. 

# Structure

There are 3 main components to the system:

`rasppi_coordinator` listens to the server and gets JSON instructions from it. 

`rasppi_listener` runs in parallel with the rasppi coordinator, it listens to the socket on localhost for instructions from `rasppi_coordinator. It is responsible for moving the lift. 

`ev3_listener` runs onboard the EV3 and handles moving aroung the warehouse using PID control, the server is not aware of how the robot moves, just that it can move n blocks.