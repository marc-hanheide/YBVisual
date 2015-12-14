/**
	Contains code for defining individual projects
	**/
	
	
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