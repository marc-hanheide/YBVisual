/*
	YBEDITOR Controller - Used for sending application data to the python server

*/


SENDING_DATA = false


/*
   ------------------------------------------------
        SERVER I/O FUNCTIONS
   ------------------------------------------------
*/
//Send application data to the server
function SendApplicationData(appdata){
	//var json = createJSON("APPDATA",appdata);
	//SendData(createJSON("APPSAVE",Application.Current,appdata));
	SendData(createJSON("APPLICATION",createJSON("SAVE",Application.Current,appdata),""))
}

//Load application data from the server
function LoadApplicationData(appname){
	
	//SendData(createJSON("APPOPEN",appname,""),function(data){
	//		alert(data);
	//});
	appxml = ''
	SendData(createJSON("APPLICATION",createJSON("OPEN",appname,""),""),function(data){
		appxml = data
		})
	return appxml
	
}

//Request a list of applications saved locally on the server
function RequestApplicationList(){

	_list = []
	SendData(createJSON("APPLICATION",createJSON("LIST","",""),""),function(data){
		json = JSON.parse(data)
		_list = json.applications
		})
	return _list
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

//Send application code data
function sendApplicationCode(code){
	var json_final = createJSON("RUN",code,"")
	SendData(json_final)
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
		
		//Also add to filter previews
		document.getElementById('camera_viewer_filter_none').src = img_src
		
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
{  $.ajax({ type:"POST",data: _data } );  request.done(function(){}) }

function SendData(_data,callback)
{  var request = $.ajax({ type:"POST",data: _data,async:false } );
request.done(callback);  }

//Request data using a GET request
function RequestData(_data)
{  alert("GET request"); $.ajax({ type:"GET",data: _data } ); }
