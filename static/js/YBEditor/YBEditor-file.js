/*
	YBEDITOR Controller - I/O functions for the currently loaded program

*/
	
	
/**
	Holds information for the currently loaded projects
	**/
var FileIO = 
{
	'Name':"newapplication", //Project name.
	'Commands':[], //Array for holding the commands
	//Create a new project -- reset the values
	'New':function() 
	{
		this.Filename = null;
		this.Commands = [];
		alert("values reset");
		
	},
	//Save the project
	'Save':function()
	{
		//We need the XML document
		var xml = Blockly.Xml.workspaceToDom(workspace);
		var _list = Blockly.Xml.domToPrettyText(xml);
		var _string = "";
		
		//We need it as one string
		for(var i = 0; i < _list.length;i++){
			_string = _string + _list[i];
		} 
		
		//Send the application data to the server
		SendApplicationData(_string);
		//Show completion message
		ShowMessage("Application successfully saved to file.");
	}
}

//Holds loaded xml data
var LOADED_XML = null;
//Used to send GET HTTP Requests
var XMLIO = new XMLHttpRequest();
//On XMLIO ready
XMLIO.onreadystatechange = function(){
	//Check status
	if (XMLIO.readyState == 4 && XMLIO.status == 200){
			//Check, and print the loaded XML data
			LOADED_XML = XMLIO.responseXML;
			alert("Loaded xml file: " + LOADED_XML);
	}
}

/**
	Function is used to load XML data using a HTTP GET request
**/
function LoadXML(src){
	//Send the request
	XMLIO.open("GET",src,true);
	XMLIO.send();
	//Return the loaded xml data
	return LOADED_XML;
}