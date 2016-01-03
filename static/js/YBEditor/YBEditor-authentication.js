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
function AuthUser(){
	SendData(createJSON("AUTHCHECK","",""),function(data){
		var auth = data;
		
		/*
			User is not authenticated
		*/
		if(auth == "NO"){

			AUTHENTICATED  =false;
			ShowMessage("This robot requires a password.. please log in");
			showLoginForm();
			
		}
		/*
			User is already authenticated - We don't need to hide content
		*/
		else{
			AUTHENTICATED = true;
			hideLoginForm();
			
		}
	});
}

/**
	Used to check the given password
	**/
function CheckPassword(){
	var given_pass = document.getElementById('pass_box').value;
	SendData(createJSON("PASSCHECK",given_pass,""),function(data){
		var auth = data;
		
		/*
			The password is not correct
		*/
		if(auth == "NO"){

			AUTHENTICATED  =false;
			showLoginForm();
			showIndicator();
			
		}
		/*
			The password is correct
		*/
		else{
			AUTHENTICATED = true;
			hideLoginForm();
			hideIndicator();
			
		}
	});
}

function CheckAdminPassword(){
		var given_pass = document.getElementById('pass_box').value;
		SendData(createJSON("PASSCHECK",given_pass,""),function(data){
		var auth = data;
		
		/*
			The password is not correct
		*/
		if(auth == "NO"){
			showLoginForm();
			$('#main_interface').hide();
			
		}
		/*
			The password is correct
		*/
		else{
			alert('correct')
			hideLoginForm();
			$('#main_interface').show();
			
			
		}
	});
}
	
	

/**
 * 	Show message with auth check
 * **/
function AuthCheck(usage){
	if(AUTHENTICATED){
		return true;
	}else
	{
		ShowError("Unable to " + usage + ", you need to login first.") 
		return false;
	}
}

/**
	Show the login form
	**/
function showLoginForm(){ $('#login_form').window('open'); }
/**
	Hide the login form
	**/
function hideLoginForm(){ $('#login_form').window('close'); }

/**
 * Show login indicator
 * 	**/
function showIndicator(){ $('#auth_indicator').show(); }

/**
 * 
 * Hide login indicator
 * **/
function hideIndicator(){ $('#auth_indicator').hide(); }
