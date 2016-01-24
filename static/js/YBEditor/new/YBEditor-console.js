/*
	YBEDITOR Console - Used for sending console data to the python server

*/
//Console loaded
$(document).ready(function(){ updateConnections(); });

//Message is shown when there are no activate connections
var NO_ACTIVE_CONNECTIONS = 'There are no active connections.';


/**
 * Functions correspond to different commands
 * 
 * **/
 //Reject all active connections
 function RejectAll(){ sendCommand('REJECTALL','','Rejected all active connections'); }
 //Reject specified connection
 function Reject(ip){ sendCommand('REJECT',ip,'Rejecting connection: '  + ip); }





/**
 *  Send a console command to the server
 * **/
function sendCommand(cmd,atts,debugmsg){
	ShowMessage("Console Command: " + cmd);
	ShowMessage(debugmsg);
	SendData(createJSON(cmd,atts,""));
	//Ensure that the connections list is correct
	updateConnections();
}


/**
 *  Create connection list row
 * **/
function createRow(connection){
var cont = document.createElement('div');
var title = document.createElement('div');
var btn = document.createElement('button');
btn.innerHTML = 'Reject';
btn.className = ' easyui-linkbutton';
btn.style = 'display:inline-block;'
btn.onclick=function(){
			Reject(connection);
}
title.innerHTML = String(connection)
									
									
cont.appendChild(title);
cont.appendChild(btn);
return cont;
}


/**
 * Update the connections list
 * **/
 function updateConnections(){
//Try and retrieve the connections list
SendData(createJSON("CONNECTIONS","",""),function(data){
	var _json = JSON.parse(data)
	var connections = _json.connections;
	var container = document.getElementById('connections_div');
							
	container.innerHTML = '';
	for(var i = 0; i < connections.length;i++){
									
									
			container.appendChild(createRow(String(connections[i])));
	}
	if(container.innerHTML == ''){
		container.innerHTML = NO_ACTIVE_CONNECTIONS;
	}
							
});
				
}; 
setInterval(updateConnections,2 * 1000);
