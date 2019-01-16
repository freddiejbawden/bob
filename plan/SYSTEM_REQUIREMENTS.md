# System Requirements
Version 1.0

This is a list of requirements for the minimum viable product. For additional requirements see [here](ADDITIONAL_FEATURES.md)

## Definitions
_drop off point_ the area where the user collects the item from

## Back-end (Server)
This is split into 2 separate parts

### Database
A database should be hosted that stores details about the storage unit. Each item needs to have it's state stored (in storage, in transport, removed by user) and it's location within the storage unit.

Another relational table will hold information about the items e.g. 'Manufacturer'.

The database should also store the location and state of the robot.

### Robot Command
When contacted by the robot, this system should look at orders and send the robot instructions
detailing how to complete an order.

For example, a user places an order for an item in location X, the robot is currently in position Y. The command system should tell the robot how to get to X from Y.

## Front-end

There should be a front end for a user to order items from.

## Robot

There are several systems that need to work together on the robot.

### Motion

The robot must be able to move from the drop off point to a set position in the storage unit.

### Item Retrieval

The robot must be able to reliably remove an item from a shelf and carry it to the drop off point.

The robot must be able to traverse a shelf vertically in order to reach items on higher shelves.

### Location Awareness

The robot should be able to identify when it is at a certain location.
