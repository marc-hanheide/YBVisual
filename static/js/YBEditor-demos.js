/*
   ------------------------------------------------
        YOUBOT CONTROL FUNCTIONS - Contains code for the youbot showcase demos
   ------------------------------------------------
*/
//Holds true if there is a demo running
var DEMO_RUNNING = "none";

/*
	Contains code for the keyboard control demo

*/
//Keyboard demo start code
function startKeyboardDemo(){ 
infoDialog("Starting keyboard demo, press ESC to stop.");
DEMO_RUNNING = "keyboard"; }

//Keyboard demo execute code
function keyboardDemo()
{	

			//Check for key presses
			//Left
			if(isKeyPressed("a")){
				//Start rotating the robot left....
				rotateLeft();
			
			}
			//Right
			else if(isKeyPressed("d")){
				//Start rotating the robot right..
				rotateRight();
			}	
			//UP
			else if(isKeyPressed("up")){
				//Start moving the robot forwards..
				moveForward();
			}	
			//Down
			else if(isKeyPressed("down")){
				//Start moving the robot backwards..
				moveBackward();
			}		
			//Escape pressed
			else if(isKeyPressed("z")){
				DEMO_RUNNING = "none";
				Halt();
				infoDialog("Stopped keyboard demo");
			}
		
	
}


/*
	Demo player
*/
setInterval(function(){
		
		//Is the keyboard demo running?
		if(DEMO_RUNNING == "keyboard"){ keyboardDemo(); }
		
},100);
