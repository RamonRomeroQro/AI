/*
3.2 Lab
Each team must program a behaviour for the robot. The behaviour must include a movement,
the drawing of a pattern, and the use of a sensor to change the behaviour.

Program:
Each team must program a different behaviour to other teams choose a specific pattern 
for movement, for instance: 
Square, circle, hexagon, spiral, infinite loop, or any pattern from your own design. 
(The objective is to learn to create complex movements which you will use in future labs.)
Use a sensor to modify the behaviour of your robot, e.g. stop, turn, change pattern, etc… 
When the sensor is triggered, the first behaviour must be interrupted immediately, and new behaviour must start.  

3.3 Report
Explain not what you did, but the ideas behind it, i.e. the reasoning behind your
decisions. Use the following questions to guide your deliberations:

What problems did you come across during the lab?
What modification would be required to turn your behaviour into a solution for any real
problem? i.e. Where could it be used and how?

3.4 Evaluation
See rubric on Schoology for the Lab hand-in

*/



#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h>  //Header file for sleep(). man 3 sleep for details. 

#include "abdrive.h"                      // Include simpletools header
#include "simpletools.h"                      // Include simpletools header
#include "ping.h"                             // Include ping header

void rectangle(){

	drive_goto(100,100);
	pause(200);
	drive_goto(26,-25);
	pause(200);
}

void triangle(){

	drive_goto(100,100);
	pause(200);
	drive_goto(34,-34);
	pause(200);
}




int main(){

while(1){


	if (ping_cm(10)>20){
		triangle();
	
			
	}else{
	
		rectangle();
	}

}




}