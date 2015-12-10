/*
 * Wait for the window to be ready
 */
$(document).ready(function()
{
    console.log("Window ready");

		
});




/*
   ------------------------------------------------
        USER INTERFACE FUNCTION CALLS
   ------------------------------------------------
*/
/**
	Run button clicked
	**/
function runClicked(obj){
	//Generate commands
	var commands = Generate();
	
	//Cycle through the commands
	for(var i = 0;i < commands.length;i++){
		
		/**
			We need to split - and parse the command string
			**/
		var command = commands[i].split(",");
		//Get the command type
		var type = command[0];
		
		//Check the type if its a move, or rotate command we need to get the direction, and amount
		if(type === "MOVE" || type === "ROTATE"){
			//Get the direction, and amount
			var direction = command[1];
			var amount = command[2];
			
			
			//  
			// We can now send this data to the python server as a JSON object
			//
			
			
		}

		
		
	}
	
}	


