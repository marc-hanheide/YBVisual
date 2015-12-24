/*

	YBEDITOR Authentication - Functions for ensuring proper authentication:
	#TODO:
	#There may be a system password defined -- the robot must ask for this password if required, then remember the user for a set period
	#Programs -- Users may not work on the same program at the same time.
	#Running - 
	
*/
//Holds true if user is authenticated
var AUTHENTICATED = false;

/**
	Do we need to display the authenticate window?
**/
function AuthenticateUser(){
	SendData("AUTHCHECK",function(data){
		var auth = data;
		
		/*
			User is not authenticated
		*/
		if(auth == "NO"){
			/*
				We need to hide the main edit area
			*/
			document.getElementById('editor_visual_content').style.display = 'none';
			toggleGettingStarted(false);
			toggleNewApplication(false);
			AUTHENTICATED  =false;
			
			
		}
		/*
			User is already authenticated - We don't need to hide content
		*/
		else{
			document.getElementById('editor_visual_content').style.display = 'block';
			toggleGettingStarted(true);
			toggleNewApplication(true);
			AUTHENTICATED = true;
			$('#login_form').window('close');
			
		}
	});
}

