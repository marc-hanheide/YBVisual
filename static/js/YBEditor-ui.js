/*
 * Wait for the window to be ready
 */
$(document).ready(function()
{
    console.log("Window ready");
    toggleSelections(SELECTIONS[CURRENT]);
	
	addMovePart('01');
	addRotatePart('02');
		
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
//New Project button
function newClicked()
{  
	yesnoDialog("New Project","Are sure you want to start a new project?",function()
	{ 
		//YES
		//SESSION.PROJECT.New();
		dialogClose();
		infoDialog("Starting new project");
	},
	function()
	{ 
		//NO
		dialogClose();
	});
}
//Open project button
function openClicked()
{ 
		moveForward();
}
//Save project button
function saveClicked()
{ 
		moveBackward();
}
//Execute button 
function executeClicked()
{
		Halt();
}
var SELECTIONS = new Array("statements","conditions","templates","demos");
var CURRENT = 0;


//Bottom bar button clicked
function selectionButtonClicked(id){ toggleSelections(id); }
//Used to toggle selections
function toggleSelections(id)
{
	for(i = 0; i < SELECTIONS.length;i++)
	{
		if(SELECTIONS[i] == id){ CURRENT = i; }
	}
	
	
	var input_string = '#' + id + '_' + 'content';
	$('#statements_content').hide();	$('#statements').css('background','darkgray');
	$('#conditions_content').hide();	$('#conditions').css('background','darkgray');
	$('#templates_content').hide();	$('#templates').css('background','darkgray');
	$('#demos_content').hide();	$('#demos').css('background','darkgray');
	$(input_string).show(); $('#' + id).css('background','lightgray');
	
}

//Use arrow keys to switch between selections
function selectionsChoose(key)
{
	if(key == 'left')
	{
		if(CURRENT > 0){ CURRENT--; }		
	}
	else if(key == 'right')
	{
		if(CURRENT < SELECTIONS.length-1){ CURRENT++; }
	}
	
	var sel = SELECTIONS[CURRENT];
	toggleSelections(sel);
}



/*
   ------------------------------------------------
        VISUAL PROGRAMMING PART FUNCTIONS
   ------------------------------------------------
*/
/*
	Add a move robot part
*/
function addMovePart(_id)
{
	//Main div
	var div = $('<div/>',
	{
		id:_id,
		class: 'vis_part vis_part_move'
	}).appendTo('#editor_visual_content');
	
	//Header
	var header = $('<h1/>',
	{
		text:'MOVE'
	}).appendTo(div);
	
	//Direction components
	var selection_header = $('</p>',{}).text("Direction:").appendTo(div);
	var selectbox = $('<select/>',{ });
	var option_left = $('<option/>',{value:'left'}).text("Left").appendTo(selectbox);
	var option_right = $('<option/>',{value:'right'}).text("Right").appendTo(selectbox);
	var option_forward = $('<option/>',{value:'forward'}).text("Forward").appendTo(selectbox);
	var option_back = $('<option/>',{value:'back'}).text("Back").appendTo(selectbox);
	selectbox.appendTo(div);
	
	//Amount components
	var selection_header = $('</p>',{}).text("Amount:").appendTo(div);
	var input = $('<input/>',{type:'text',name:'amount',value:'0'}).appendTo(div);
	
	//The part needs to be draggable
	partIsDraggable(div);
}

/*
	Add a rotate robot part
*/
function addRotatePart(_id)
{
	//Main div
	var div = $('<div/>',
	{
		id:_id,
		class: 'vis_part vis_part_rot'
	}).appendTo('#editor_visual_content');
	
	//Header
	var header = $('<h1/>',
	{
		text:'ROTATE'
	}).appendTo(div);
	
	//Direction components
	var selection_header = $('</p>',{}).text("Direction:").appendTo(div);
	var selectbox = $('<select/>',{ });
	var option_left = $('<option/>',{value:'left'}).text("Left").appendTo(selectbox);
	var option_right = $('<option/>',{value:'right'}).text("Right").appendTo(selectbox);
	selectbox.appendTo(div);
	
	//Amount components
	var selection_header = $('</p>',{}).text("Amount:").appendTo(div);
	var input = $('<input/>',{type:'text',name:'amount',value:'0'}).appendTo(div);
	
	//The part needs to be draggable
	partIsDraggable(div);
}


/*
	Make a part draggable
*/
function partIsDraggable(div)
{
	//Make div draggable
	//Should be contained in visual area
	//Add a grid (10 x 10)
	div.draggable({containment:"#editor_visual_content",cursor:"crosshair",grid:[10,10]});
}




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


