/*
	YBEDITOR UI- I/O - Functions to define the user interface

*/
USING_CAMERA_VIEWER = false;

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
isDocumentReady(function(){
	//Set default block
	Blockly.Xml.domToWorkspace(workspace,document.getElementById('default_blocks'))
	//Needs to handle camera viewer close event
	$('#camera_viewer').window({ collapsible:false,minimizable:false,maximizable:false,resizable:false,onBeforeClose:function(){USING_CAMERA_VIEWER=false},
		tools:[{iconCls:'icon-cancel',handler:function(){ 
			alert('exit')
			USING_CAMERA_VIEWER = false
			}}]  })
	//Set application title
	Application.SetTitle()
	toggleApplications(false)
	toggleApplicationSaveWindow(false)
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
function toggleNewApplication(flag){
	if(flag){
		$('#new_app').window('open');
	}else{
		$('#new_app').window('close');
	}
}
function toggleCameraViewer(flag){
	if(flag){
		$('#camera_viewer').window('open');
	}else{
		$('#camera_viewer').window('close');
	}
}
function toggleApplications(flag){
	if(flag){
		$('#applications_window').window('open');
	}else{
		$('#applications_window').window('close');
	}
}
function toggleApplicationSaveWindow(flag){
	if(flag){
		$('#applications_save').window('open');
	}else{
		$('#applications_save').window('close');
	}
}

function clearApplications(){ document.getElementById('applications_select').innerHTML = "" }
function addApplication(name){
	document.getElementById('applications_select').innerHTML += "<option value=" + "'" + name + "'" + ">" + name + "</option>"
}
function getSelectedApplication(){
	var select = document.getElementById('applications_select')
	var selected = select.options[select.selectedIndex].value
	return selected
}


var CURRENT_DEMO = ' '
var DEMO_RUNNING = false
function showDemoWindow(){
	toggleDemoWindow(true)
	DEMO_RUNNING = true
}
function closeDemoWindow(name){
	SendDemoStopRequest()
	toggleDemoWindow(false)
	DEMO_RUNNING = false
	CURRENT_DEMO = ' '
}	
function toggleDemoWindow(flag){
	if(CURRENT_DEMO!=' '){
		if(flag){
			$('#demo_window').window('open');
		}else{
			$('#demo_window').window('close');
		}
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
	Application.New()
}

/**
	Save button clicked
		**/
function saveClicked(type){
	if(type===0){
		Application.Save()
	}else if(type===1){
		toggleApplicationSaveWindow(true)
	}else{
		var appname = document.getElementById('app_name').value;
		Application.SetName(appname);
		Application.Save(); 
		toggleApplicationSaveWindow(false)
	}
	
	
}

/**
	Open button clicked
	**/
function openClicked(){
	Application.Saved()
	
}


/**
	Run button clicked
	**/
function runClicked(obj){
	
		//generate code
		var code = ""
		code = String(Blockly.Python.workspaceToCode(workspace))

		/**
			We need to check if the commands were generated successfully
		**/
		if(code!=""){
				ShowMessage("Robot commands generated. Executing Program..");
			
				//Send command data to the server as a JSON

				sendApplicationCode(code);
		
		}else{ ShowError("Unable to run program,caused by an error generating robot commands. You either created too many STARTROBOT blocks, or you need to create one."); }
	
	
}	
/**
	Stop button clicked
	**/
function stopClicked(obj){

		SendStopCommand();
		ShowMessage("Robot stopped successfully.");
	
	
}
/**
	Demo button clicked
	**/
function demoClicked(obj,demo_name){

		CURRENT_DEMO = demo_name + '_cont' 
		ShowMessage("Starting demo: " + demo_name);
		SendDemoStartRequest(demo_name)
		showDemoWindow()
	
}

function cameraProcLoop(){
			if(USING_CAMERA_VIEWER==true){SendCameraViewRequest()}
} 			setInterval(cameraProcLoop,500);

/**
 *  Camera button clicked
 * **/
function cameraButtonClicked(){
	toggleCameraViewer(true)
	USING_CAMERA_VIEWER = true
}


/*
   ------------------------------------------------
      KEYBOARD INPUT FUNCTIONS
   ------------------------------------------------
*/
//shift+n = new application
Mousetrap.bind('shift+n',newClicked)
//shift+o = open application
Mousetrap.bind('shift+o',openClicked)
//shift+s = save application
Mousetrap.bind('shift+s',saveClicked)
//shift+r = run
Mousetrap.bind('shift+r',runClicked)
//shift+c = shutdown
Mousetrap.bind('shift+c',function(){
	SendServerRequest("SHUTDOWN")
});
//shift+1 = Open camera viewer
Mousetrap.bind('shift+1',cameraButtonClicked)
//ESC == close opened window
Mousetrap.bind('escape',function(){
	console.log('escape pressed')
	if(DEMO_RUNNING){
		SendDemoStopRequest()
		closeDemoWindow()
	}
	if(USING_CAMERA_VIEWER){
		toggleCameraViewer()
		USING_CAMERA_VIEWER = false
	}
	
	//If escape is pressed -- a stop command must be sent to the robot
	SendStopCommand()
	ShowMessage("Robot stopped successfully.");
});


	
	








