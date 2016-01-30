/*

	YBEDITOR Blocks - Contains definitions,and handling for blocks
*/

//START ROBOT
////https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#svhneq
Blockly.Blocks['start_robot'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("START ROBOT");
    this.setNextStatement(true);
    this.setColour(100);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
}; START_COLOUR = 100

//MOVE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#cckrgt
Blockly.Blocks['move'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(" MOVE")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"], ["forwards", "FORWARDS"], ["back", "BACK"]]), "DIRECTION")
        .appendField("amount")
        .appendField(new Blockly.FieldTextInput("0"), "AMOUNT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('Move the robot by amount, in specified direction');
    this.setHelpUrl('http://ybvisual.adamwcs.co.uk');
  }
}; MOVE_COLOUR = 210

//ROTATE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#mbz6sk
Blockly.Blocks['rotate'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("ROTATE")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]), "DIRECTION")
        .appendField("amount")
        .appendField(new Blockly.FieldTextInput("0"), "AMOUNT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(220);
    this.setTooltip('Rotate the robot by amount, in specified direction');
    this.setHelpUrl('http://ybvisual.adamwcs.co.uk');
  }
}; ROTATE_COLOUR = 220
 
//ROTATE JOINT
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#n9qvsj
Blockly.Blocks['rotate_joint'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("ROTATE JOINT")
        .appendField(new Blockly.FieldDropdown([["arm_joint_1", "arm_joint_1"], ["arm_joint_2", "arm_joint_2"], ["arm_joint_3", "arm_joint_3"], ["arm_joint_4", "arm_joint_4"], ["arm_joint_5", "arm_joint_5"]]), "ID")
        .appendField("amount")
        .appendField(new Blockly.FieldTextInput("0"), "AMOUNT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Rotate specified joint by given joint space value');
    this.setHelpUrl('http://ybvisual.adamwcs.co.uk');
  }
}; ROTATE_JOINT_COLOUR = 300

//MOVE ARM PRE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#j8ting
Blockly.Blocks['move_arm_pre'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("MOVE ARM")
        .appendField(new Blockly.FieldTextInput("position name.."), "POSNAME");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(310);
    this.setTooltip('Move arm to pre-defined position (E.G candle,folded)');
    this.setHelpUrl('http://ybvisual.adamwcs.co.uk');
  }
}; MOVE_ARM_PRE_COLOUR = 310

//GRIPPER STATUS
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#j8ting
Blockly.Blocks['gripper_status'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("GRIPPER")
        .appendField(new Blockly.FieldDropdown([["OPEN", "GRIPPER_OPEN"], ["CLOSE", "GRIPPER_CLOSE"]]), "GRIPPER_STATUS");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(350);
    this.setTooltip('Set gripper status');
    this.setHelpUrl('http://ybvisual.adamwcs.co.uk');
  }
}; GRIPPER_STATUS_COLOUR = 350

//IF GRIPPER STATE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#aa6qba
Blockly.Blocks['if_gripperstate'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("IF")
        .appendField("GRIPPER STATE")
        .appendField(new Blockly.FieldDropdown([["CLOSED", "CLOSED"], ["OPEN", "OPEN"]]), "GRIPPER_S")
        .appendField("THEN");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(1);
    this.setTooltip('IF condition - checks gripper state');
    this.setHelpUrl('http://ybvisual.adamwcs.co.uk');
  }
}; GRIPPER_STATE_COLOUR = 1

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
		if(col===MOVE_COLOUR){
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
		if(col===ROTATE_COLOUR){
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
		if(col===ROTATE_JOINT_COLOUR){
			//Get joint id
			var jointid = block.getFieldValue('ID');
				
			//Get amount
			var amount = block.getFieldValue('AMOUNT');
			
			//Push to the commands array
			commands.push("ROTATEJOINT," + jointid + "," + amount);
		}
		//Move arm to pre-defined position command
		if(col===MOVE_ARM_PRE_COLOUR){
			//Get defined position name
			var posname = block.getFieldValue('POSNAME')
			
			//Push to the commands array
			commands.push("MOVEARM," + "DEFPOS" + "," + posname);
		}
		//Toggle gripper status
		if(col==GRIPPER_STATUS_COLOUR){
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
		if(col==GRIPPER_STATE_COLOUR){
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

