/*
	YBEDITOR UI- I/O - Functions to define the user interface

*/

/*
   ------------------------------------------------
       INTERFACE STYLE FUNCTIONS
   ------------------------------------------------
*/
//Holds available stylesheets
var THEMES = 
[
	['metro','/static/css/themes/metro/easyui.css'],
	['gray','/static/css/themes/gray/easyui.css'],
	['default','/static/css/themes/default/easyui.css'],
	['bootstrap','/static/css/themes/bootstrap/easyui.css'],
	['black','/static/css/themes/black/easyui.css']
];
//Changes page style
function changeStyle(name){	
	var theme = null;
	
	for(var i = 0; i < THEMES.length;i++){
		
		if(THEMES[i][0] == name){
			theme = THEMES[i][1];
		}
	}
	
	if( !(theme==null) ){
		document.getElementById('ui_style').href = theme;
	}
	
}


/*
 * Wait for the window to be ready
 */

function isDocumentReady(func){
	$(document).ready(func);
}


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
function toggleNewApplication(flag){
	if(flag){
		$('#new_app').window('open');
	}else{
		$('#new_app').window('close');
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
function newClicked(ask){
if(AuthCheck("create new application")){
		if(ask)
		{
			Confirm("Are you sure you would like to create a new project? you will lose any unsaved changes.",
			function(){
			/*
				User clicked YES
			*/
				FileIO.New();
				toggleNewApplication(true);
		
			},function(){
			/*
				User clicked NO
			*/
		
			});
		}else{ toggleNewApplication(true); }
}
}

/**
	Save button clicked
		**/
function saveClicked(){
	if(AuthCheck("save application")){
		FileIO.Save();
	}
	
}

/**
	Open button clicked
	**/
function openClicked(){
	if(AuthCheck("open application")){
		FileIO.Open();
	}
}


/**
	Run button clicked
	**/
function runClicked(obj){
	if(AuthCheck("run application")){
		//Generate commands
		var commands = Generate();
	
		/**
			We need to check if the commands were generated successfully
		**/
		if(commands.length>0){
				ShowMessage("Robot commands generated. Executing Program..");
			
				//Send command data to the server as a JSON
				sendApplicationJSON(commands);
		
		}else{ ShowError("Unable to run program,caused by an error generating robot commands. You either created too many STARTROBOT blocks, or you need to create one."); }
	}
	
}	
/**
	Stop button clicked
	**/
function stopClicked(obj){
	if(AuthCheck("stop robot")){
		SendStopCommand();
		ShowMessage("Robot stopped successfully.");
	}
	
}
/**
	Demo button clicked
	**/
function demoClicked(obj,demo_name){
	if(AuthCheck("start demo: " + demo_name)){
		ShowMessage("Starting demo: " + demo_name);
	}
}







