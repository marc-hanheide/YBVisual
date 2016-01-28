//START ROBOT
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#svhneq
Blockly.JavaScript['start_robot'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

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

//ROTATE JOINT
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#n9qvsj
Blockly.JavaScript['rotate_joint'] = function(block) {
  var dropdown_id = block.getFieldValue('ID');
  var text_amount = block.getFieldValue('AMOUNT');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};


//MOVE ARM PRE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#j8ting
Blockly.JavaScript['move_arm_pre'] = function(block) {
  var text_posname = block.getFieldValue('POSNAME');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};


//GRIPPER STATUS
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#j8ting
Blockly.JavaScript['gripper_status'] = function(block) {
  var dropdown_gripper_status = block.getFieldValue('GRIPPER_STATUS');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};


//IF GRIPPER STATE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#aa6qba
Blockly.JavaScript['if_gripperstate'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};




/*
	Used to convert the program into workable data
*/
function Generate(){
	
	//Get the block collection
	var blocks = getBlockArray(100);
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
		if(col === 110){
			//Get direction
			var dir = block.getFieldValue('DIRECTION');
			//Get amount
			var amount = block.getFieldValue('AMOUNT');
			
			//For debugging
			//alert('move found');
			
			//Push to the commands array
			commands.push("MOVE," + dir + "," + amount);
			
		}
		//Rotate command type
		if(col===220){
			//Get direction
			var dir = block.getFieldValue('DIRECTION');
			//Get amount
			var amount = block.getFieldValue('AMOUNT');
			
			//For debugging
			//alert('rotate found');
			
			//Push to the commands array
			commands.push("ROTATE," + dir + "," + amount);
		}
		//Rotate joint command
		if(col===300){
			//Get joint id
			var jointid = block.getFieldValue('ID');
				
			//Get amount
			var amount = block.getFieldValue('AMOUNT');
			
			//Push to the commands array
			commands.push("ROTATEJOINT," + jointid + "," + amount);
		}
		//Move arm to pre-defined position command
		if(col===310){
			//Get defined position name
			var posname = block.getFieldValue('POSNAME')
			
			//Push to the commands array
			commands.push("MOVEARM," + "DEFPOS" + "," + posname);
		}
		//Toggle gripper status
		if(col==350){
			//Get chosen status
			var grip_status = block.getFieldValue('GRIPPER_STATUS');
			grip_status = grip_status.split("_")[1]
			
			//Push to the commands array
			commands.push("GRIPPER," + "SET" + "," + grip_status);
		}

		// ---
		// CONDITIONS
		// ---

		//Gripper state condition
		if(col==1){
			//Which gripper state is being checked
			var gripper_cond = block.getFieldValue("GRIPPER_S")
			//Push to the commands array
			commands.push("COND," + "GRIPPERSTATE" + "," + gripper_cond)
		}
		
	}
	
	
	/*
		Finally - the function should return the final commands list
	*/
	return commands;
}


/**
	Used to get blocks, and store in array
**/
function getBlockArray(top_col){
	//Get top blocks
	var blocks = workspace.getTopBlocks(true);
	//This will hold the start robot blocks
	var start_blocks = [];
	
	//Cycle through the top blocks
	for(var i = 0; i < blocks.length;i++){
		//Check the colour of the block.. is it a start_robot block?
		if(blocks[i].getColour()===top_col){
			//If true, add to the array
			//start_blocks = blocks[i];
			start_blocks.push(blocks[i]);
		}
	}
	//Only return valid if:
	//1. A START_ROBOT block was created
	//2. The block is valid
	//3. Only one START_ROBOT block exists
	if( (start_blocks.length===1))
	{
		blocks = start_blocks;
	
		//Get all blocks -- including children
		for(var i = 0; i < blocks.length;i++){
			blocks = blocks.concat(blocks[i].getChildren());
		
		}
	
		//Return block contents
		return blocks;
		
	}else{  
	return start_blocks; } 
}





