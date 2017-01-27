/*
	YBEDITOR File - I/O functions for the currently loaded application

*/

/**
 *  Holds information regarding the current application
 * **/
var Application = 
{
	//The current application
	'Current':'untitled',
	'SetName':function(_new){
		Application.Current = _new
		Application.SetTitle()
	},
	//Start a new application
	'New':function(){
		workspace.clear()
		Blockly.Xml.domToWorkspace(workspace,document.getElementById('default_blocks'))
		Application.SetTitle()
	},
	'_New':function(appname,xmldom){
		workspace.clear()
		Blockly.Xml.domToWorkspace(workspace,xmldom)
		Application.SetName(appname)
		toggleApplications(false)
	},
	//Open an existing application
	'Open':function(application){
		appdata = LoadApplicationData(application)
		var xml = Blockly.Xml.textToDom(appdata)
		Application._New(application,xml)
	},
	//Save the current application to file
	'Save':function(){
		//Gather the XML document
		var xml = Blockly.Xml.workspaceToDom(workspace)

		
		var xml_text = Blockly.Xml.domToText(xml)
		
		//Send the application data to the server
		SendApplicationData(xml_text);
		//Show completion message
		ShowMessage("Application successfully saved to file.");
	},
	//Return a list of the currently saved applications
	'Saved':function(){ list = RequestApplicationList(); 
		//Get list of saved applications
		apps = list
		clearApplications()
		for(i in apps){
			app = apps[i]
			addApplication(app)
		}
		toggleApplications(true)
		 },
	//Set application window title
	'SetTitle':function(){ document.title = "YouBot Visual: " + Application.Current }
};


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
