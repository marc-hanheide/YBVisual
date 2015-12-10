/*
 * Wait for the window to be ready
 */
$(document).ready(function()
{
    console.log("Window ready");

		
});



/*
   ------------------------------------------------
        DIALOG FUNCTIONS
   ------------------------------------------------
*/

/*
  Display a yes/no dialog box
*/
function yesnoDialog(title,desc,func_yes,func_no)
{
	$('#dialog').prop('title',title); //Set dialog title
	$('#dialog_desc').text(desc); //Set dialog description
	
	/*
		Create the dialog
	*/
	$('#dialog').dialog(
   {
	   resizable: false, /* We shouldn't be able to resize the dialog */
	   /*
			-- DIALOG BUTTONS --
	   */
	   buttons:
	   [
	   { text: "YES", click:func_yes }, /* Yes button  */
	   { text:"NO", click:func_no } /* No button */
	   ] 
   }
   );
}

/*
	Display a basic information dialog
*/
function infoDialog(info)
{
	$('#dialog').prop('title',"Robot Info"); //Set dialog title
	//Set dialog information/description
	$('#dialog_desc').text(info); 
	
	/*
		Create the dialog
	*/
	$('#dialog').dialog(
	{
		//Shouldn't be resizable
		resizable: false,
		//Add an OKAY button
		buttons:[{text:"OKAY",click:dialogClose}]
	}
	);
}

/* Close the currently opened dialog */
function dialogClose(){ $('#dialog').dialog("close");  }



/*
   ------------------------------------------------
        USER INTERFACE FUNCTION CALLS
   ------------------------------------------------
*/
function runClicked(obj){
	Generate();
}


/*
   ------------------------------------------------
        VISUAL PROGRAMMING PART FUNCTIONS
   ------------------------------------------------
*/




/*
   ------------------------------------------------
        KEY PRESS FUNCTIONS
   ------------------------------------------------
*/
//Function is used to check if a key is pressed
function isKeyPressed(key){
		if(key == LAST_KEY_PRESSED_CHAR || key.toUpperCase() == LAST_KEY_PRESSED_CHAR ){
			return true;
		}else{
			return false;
		}
}


var LAST_KEY_PRESSED_CODE = null;
var LAST_KEY_PRESSED_CHAR = null;
$(document).keypress(function(e)

{
	LAST_KEY_PRESSED_CODE = e.keyCode;
	LAST_KEY_PRESSED_CHAR = String.fromCharCode(e.which);

	
	//Left key press
	if(e.keyCode == 37){ 
	selectionsChoose('left');
	LAST_KEY_PRESSED_CHAR = 'left';
	}
	//Right key press
	if(e.keyCode == 39){ 
	selectionsChoose('right');
	LAST_KEY_PRESSED_CHAR = 'right';
	}
	//Up key press
	if(e.keyCode == 38){
		LAST_KEY_PRESSED_CHAR = 'up';
	}
	//Down key press
	if(e.keyCode == 40){
		LAST_KEY_PRESSED_CHAR = 'down';
	}
	
	
});
$(document).keydown(function(e){
	//Left key press
	if(e.keyCode == 37){ 
	LAST_KEY_PRESSED_CHAR = 'left';
	}
	//Right key press
	if(e.keyCode == 39){ 
	LAST_KEY_PRESSED_CHAR = 'right';
	}
	//Up key press
	if(e.keyCode == 38){
		LAST_KEY_PRESSED_CHAR = 'up';
	}
	//Down key press
	if(e.keyCode == 40){
		LAST_KEY_PRESSED_CHAR = 'down';
	}
});
$(document).keyup(function(e){
	LAST_KEY_PRESSED_CODE = -1;
	LAST_KEY_PRESSED_CHAR = '';
});


