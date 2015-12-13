/*
 * Wait for the window to be ready
 */
$(document).ready(function()
{
	//Initially - we don't want to see the 'getting started' window
	toggleGettingStarted(false);
		
});
/*
   ------------------------------------------------
       INTERFACE WINDOW FUNCTIONS
   ------------------------------------------------
*/
function toggleGettingStarted(flag){
	if(flag){
		$('#getting_started').window('open');
	}else{
		$('#getting_started').window('close');
	}
}



/*
   ------------------------------------------------
        MESSAGER FUNCTIONS
   ------------------------------------------------
*/
/**
	Show message with given message, and timeout
	**/
function ShowMessage(_msg){
	var date = new Date();
	
	$.messager.show(
	{
			title:'Notification',
			msg:date + ' - ' + _msg,
			timeout:2000,
			showType:'show'
		
	});
}
function ShowError(_msg){
	var date = new Date();
	$.messager.alert('ERROR',date + ' - '  +_msg);
}
function Confirm(_msg,func_yes,func_no){
	$.messager.confirm('YB Visual',_msg,function(flag){
		if(flag){
			func_yes();
			
		}else{ func_no(); }
		
	});
}



/*
   ------------------------------------------------
        USER INTERFACE FUNCTION CALLS
   ------------------------------------------------
*/
/**
	New button clicked
	**/
function newClicked(){
	Confirm("Are you sure you would like to create a new project? you will lose any unsaved changes.",
	function(){
		/*
			User clicked YES
		*/
		
	},function(){
		/*
			User clicked NO
		*/
		
	});
}



/**
	Run button clicked
	**/
function runClicked(obj){
	//Generate commands
	var commands = Generate();
	
	/**
		We need to check if the commands were generated successfully
	**/
	if(commands.length>0){
			ShowMessage("Robot commands generated. Executing Program..");
	
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
			
				//If move command - move the robot in direction, by amount
				if(type == "MOVE"){
				
				}
				//If rotate command - rotate the robot in direction,by amount
				if(type == "ROTATE"){
				
				}
			
			
			}

		
		
		}
	}else{ ShowError("Unable to run program,caused by an error generating robot commands. You either created too many STARTROBOT blocks, or you need to create one."); }
	
}	
/**
	Stop button clicked
	**/
function stopClicked(obj){
	ShowMessage("Robot stopped successfully.");
	
}
/**
	Demo button clicked
	**/
function demoClicked(obj,demo_name){
	ShowMessage("Starting demo: " + demo_name);
}








