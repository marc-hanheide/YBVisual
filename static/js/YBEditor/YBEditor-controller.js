


/*
   ------------------------------------------------
        SERVER I/O FUNCTIONS
   ------------------------------------------------
*/
//Send application data to the setActive
function SendApplicationData(appdata){
	//var json = createJSON("APPDATA",appdata);
	SendData(createJSON("APPDATA",FileIO.Name,appdata));
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
	
	//Create a final JSON object using the created json array
	var json_final = JSON.stringify(data);
	//Created -- now send the JSON object to the server
	SendData(json_final);
	
}


//Send data as POST request
function SendData(_data)
{  $.ajax({ type:"POST",data: _data } ); }