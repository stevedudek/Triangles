# Triangles Documentation

August 15, 2016
<br>

## Sections

* #### Triangle Installation
* #### Hardware Connections
* #### Starting the Software
* #### Configuring the Triangles
* #### Running the Software
* #### Show Controls
* #### New Year's Eve event
* #### Technical Notes

## Triangles Installation

For each Triangle, the orientation of the one connecting wire (i.e. which corner) does not matter. Also does not matter which side of the Triangle faces front.

It is easiest to position the corner with the connecting wire closest to the Pixel Pusher to use the least amount of wire.

I prefer to suspend the Triangles with rope tied securely looped around the corner hinges. If you are hanging a Triangle over a crowd, suspend from at least two corners as a wood rail could tear off from a hinge. If you screw eye-bolts into the wood rails, pre-drill the hole (really), or you will split the wood.

Don't unloop the connection wire from the Triangle corner. The wire is looped once to relieve strain and prevent tearing the electronic connection.

## Hardware Connections

### Triangles

Connect block-terminal extender cables as needed to wire the Triangles to a centralized spot where the following lives together: Pixel Pusher, power supply, router, and laptop.

The extender cables have male and female ends much like extension cords.

Plug the cables into the Pixel Pusher ports. When disconnecting a cable from the Pusher, disconnect it at the block junction and not at the Pusher. The pins on the Pusher are fragile, and if we mush them, we're screwed.

### Pixel Pusher

The Pusher has 7 connectors already seated: 6 you need and 1 extra. You can read the strip numbers in white letters on the Pusher, like "Strip 1."

I set up the 6 Triangles in this configuration to make 2 hourglasses and a middle diamond. I suggest hanging that middle diamond sideways over the middle of the dance floor.


### USB Stick

No USB Stick needed. The Pixel Pusher is already hardware configured

### Router

Plug the router into a power strip with the included wallwart adapter. Your computer needs to talk to the wired router with these settings:

![image](pixelpusher-net.jpeg)

If you are set up right, you should be able to type "ping 10.1.0.20" from the Terminal and see a response

### Computer

Plug the computer's power into that power strip.

Connect a 2nd ethernet cable from the computer to the router. I have been using port 1.

### Power Supply

Plug in the silver 40A power supply. A green light should come on in the power supply. Plug the power supply into the Pixel Pusher.

## Starting the Software

Boot up a text editor, like Sublime Text. Boot up Processing.

Open "triangle.py" in the text editor and "TriangleSimulatorAndLighter.pde" in Processing.

These are the two files you need to run the Triangles. All the files live in a folder called Triangle. The file structure on my laptop looks like:

![image](File_Structure.png)

## No Need to Configure the Triangles

You don't need to configure the positions of the Triangles, but if you wanted to, do the following. Tell the software how each Triangle is oriented

#### TriangleSimulatorAndLighter.pde

Boot up Processing. Open the TriangleSimulatorAndLighter.

## Running the Software

In Processing, press the triangle arrow to start the TriangleSimulatorAndLighter. It should boot java to present the Triangle simulator (see picture in Show Controls section).

Open a terminal. Switch to the Triangle directory. For me, this means first typing:

	$ cd Triangle

Type:

	$ python go.py

![image](Terminal_ScreenShot.png)

The simulator should display the display the current show. The Triangles should light up. Check the Triangle lights against the Simulator to see whether you read the connections correctly.

## Show Controls

You can change the lighting in the following ways:

### Toggle Labels

Click the empty box to toggle the display on the Simulator for (x,y) coordinates and (strip, pixel) coordinates, useful if you forget how the coordinate system works or where each Big Triangle lives.

### Brightness

That bold 100 is % Brightness. You can dial down the brightness to 10%. Background pixels take longer to refresh brightness so brightness changes may not be immediately apparent for all pixels.

### Color

Only one of the 7 boxes can be checked at a time. Checking the large white box means no color correction. Color correction is useful to warm the display into reds and yellows. Try color correction before show time so you know what you are getting into.

##### None

Exclude this color from the palette.

##### All

Always present this color.

### Shows

Shows are picked randomly and run for 3 minutes (180 seconds). If you want longer or shorter shows, run a different script command with the time in seconds (60 seconds shown below):

	python go.py --max-time 60

### Screen Shot of the Simulator

![image](Simulator_ScreenShot.png)

	
## Technical Notes

### Contact infomation

##### Stephen Dudek
781-223-8626
stevedudek@gmail.com

##### John Major
617-270-7981
iamh2o@gmail.com

