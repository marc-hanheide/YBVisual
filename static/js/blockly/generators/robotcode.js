/*
	Contains definitions for converting blocks to robot code

*/
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
	
	/**
		Cycle through, and check each block
	**/
	for(var i = 0; i  < blocks.length;i++){
		//We need to get the blocks type
		blocks[i].select();
		var col = blocks[i].getColour();
		
		
		/**
			We can use the blocks colour to check its type
		**/
		if(col === 210){
			alert("found move command");
		}
		if(col===220){
			alert("found rotate command");
		}
		
	}
	
	
}


/**
	Used to get blocks, and store in array
**/
function getBlockArray(){
	var blocks = workspace.getTopBlocks(true);
	
	for(var i = 0; i < blocks.length;i++){
		blocks = blocks.concat(blocks[i].getChildren());
		
	}
	
	return blocks;
}





