/*
	YBEDITOR Controller - Used for sending application data to the python server

*/





/*
   ------------------------------------------------
        SERVER I/O FUNCTIONS
   ------------------------------------------------
*/
//Send application data to the server
function SendApplicationData(appdata){
	//var json = createJSON("APPDATA",appdata);
	SendData(createJSON("APPSAVE",FileIO.Name,appdata));
}

//Load application data from the server
function LoadApplicationData(appname){
	
	SendData(createJSON("APPOPEN",appname,""),function(data){
			alert(data);
	});
	
}

//Request a list of applications saved locally on the server
function RequestApplicationList(){
	
	SendData(createJSON("APPLIST","",""),function(data){
			alert(data);
	});
	
} 

//Create JSON data to send to the server
function createJSON(_type,_att,_val){
	var obj = new Object();
	obj.type = _type;
	obj.attribute = _att;
	obj.value = _val;
	var _json = JSON.stringify(obj);
	return _json;
}

//Create the JSON application data to send to the server
function sendApplicationJSON(commands){
	//Array holds the gathered JSON objects
	//var commands_json = [];
	var data = new Object();
	data.commands = [];
	
	console.log('Sending application JSON')
	
	//Cycle through the commands
	for(var i = 0;i < commands.length;i++){
		
		/**
			We need to split - and parse the command string
		**/
		var command = commands[i].split(",");
		//Get the command type
		var type = command[0]; 
		//Get command attributes
		var attribute = command[1]; 
		//Get command value
		var val = command[2];
		//From these - we can create the JSON object
		var _json = createJSON(type,attribute,val);
		//Add to the array
		data.commands.push(_json);
	
	}
	
	//Finally -- add a halt command
	var json_halt = createJSON("HALT","","");
	data.commands.push(json_halt);
	
	//Create a final JSON object using the created json array
	//var json_final = JSON.stringify(data);
	var json_final = createJSON("RUN",JSON.stringify(data),"")
	//Created -- now send the JSON object to the server
	SendData(json_final);
	
}

//Send a stop command to the robot
function SendStopCommand(){
	var data = new Object();
	data.commands = [];
	
	var type = "ESTOP"
	var attribute = ""
	var val = ""
	var _json = createJSON(type,attribute,val)
	
	SendData(_json)
}

//Send a demo start request
function SendDemoStartRequest(name){
	var data = new Object();
	data.commands = [];
	var demo_json = createJSON("DEMO","START",name)
	data.commands.push(demo_json)
	var json_final = createJSON("RUN",JSON.stringify(data),"")
	SendData(json_final)
}
//Send a demo stop request
function SendDemoStopRequest(){
	var data = new Object();
	data.commands = [];
	var demo_json = createJSON("DEMO","STOP","")
	data.commands.push(demo_json)
	var json_final = createJSON("RUN",JSON.stringify(data),"")
	SendData(json_final)
}

//Send a camera view request
function SendCameraViewRequest(){
	var type = "SENSORS"
	var attribute = "CAMERA"
	var val = "VIEW"
	var _json = createJSON(type,attribute,val)
	SendData(_json,function(data){
		img_src = 'data:image/jpg;base64,'+data+''
		document.getElementById('camera_viewer_src').src = img_src
		})
}

//Send a key event
function SendKeyEvent(type,key){
	var _type = ''
	if(type==="PRESS"){
		_type = 'PRESS'
	}else{ _type = 'RELEASE' }
	
	SendData(createJSON("KEYEVENT",_type,key))
}

//Send sever control command
function SendServerRequest(type){
	var _json = createJSON("SERVER",type,"")
	SendData(_json)
}


//Send data as POST request
function SendData(_data)
{  $.ajax({ type:"POST",data: _data } ); }

function SendData(_data,callback)
{  var request = $.ajax({ type:"POST",data: _data } );
request.done(callback);  }

//Request data using a GET request
function RequestData(_data)
{  alert("GET request"); $.ajax({ type:"GET",data: _data } ); }
