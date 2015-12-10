
//MOVE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#8fk3o3
Blockly.JavaScript['move'] = function(block) {
  var dropdown_direction = block.getFieldValue('DIRECTION');
  var text_amount = block.getFieldValue('AMOUNT');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

//ROTATE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#mbz6sk
Blockly.JavaScript['rotate'] = function(block) {
  var dropdown_direction = block.getFieldValue('DIRECTION');
  var text_amount = block.getFieldValue('AMOUNT');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};


/*
	Used to convert the program into workable data
*/
function Generate(){
	
	//Get the block collection
	var blocks = getBlockArray();
	//We need a collection which contains the final commands
	var commands = [];
	
	
	/**
		Cycle through, and check each block
	**/
	for(var i = 0; i  < blocks.length;i++){
		//We need to get the blocks type
		var block = blocks[i];
		block.select();
		var col = block.getColour();
		
		/**
			We can use the blocks colour to check its type
		**/
		//Move command type
		if(col === 210){
			//Get direction
			var dir = block.getFieldValue('DIRECTION');
			//Get amount
			var amount = block.getFieldValue('AMOUNT');
			
			//Push to commands array
			//commands.push({
			//	'type':'MOVE',
			//	'direction':dir,
			//	'amount':amount
			//});
			commands.push("MOVE," + dir + "," + amount);
			
		}
		//Rotate command type
		if(col===220){
			//Get direction
			var dir = block.getFieldValue('DIRECTION');
			//Get amount
			var amount = block.getFieldValue('AMOUNT');
			
			//Push to commands array
			//commands.push({
			//	'type':'ROTATE',
			//	'direction':dir,
			//	'amount':amount
			//});
			commands.push("ROTATE," + dir + "," + amount);
		}
		
	}
	
	
	/*
		Finally - the function should return the final commands list
	*/
	//for(var i = 0 ; i < commands.length;i++){
	//	alert(commands[i]);
	//}
	return commands;
}


/**
	Used to get blocks, and store in array
**/
function getBlockArray(){
	//Get top blocks
	var blocks = workspace.getTopBlocks(true);
	
	//Get all blocks -- including children
	for(var i = 0; i < blocks.length;i++){
		blocks = blocks.concat(blocks[i].getChildren());
		
	}
	
	//Return block contents
	return blocks;
}





