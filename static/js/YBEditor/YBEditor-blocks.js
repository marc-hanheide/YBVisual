/*

	YBEDITOR Blocks - Contains definitions,and handling for blocks
*/
//The help URL for all YBEditor blocks
HELP_URL =  'http://ybvisual.adamwcs.co.uk'

/*
 * Contains identification strings for each block
 * */
RBLOCKS = {
	 //Start robot block
	'start_robot':{ id:'start_robot',output:function(block){return RBLOCKS.createcommand("","","")}},
	//Move robot
	'move':{ id:'move',output:function(block){ 
			return RBLOCKS.createVelCommand("MOVE",block.getFieldValue("DIRECTION"),block.getFieldValue("AMOUNT"))
		} },
	//Rotate robot
	'rotate':{ id:'rotate',output:function(block){ 
			return RBLOCKS.createVelCommand("ROTATE",block.getFieldValue("DIRECTION"),block.getFieldValue("AMOUNT"))
		} },
	//Rotate joint
	'rotate_joint':{ id:'rotate_joint',output:function(block){ 
			return RBLOCKS.createcommand("ROTATEJOINT",block.getFieldValue("ID"),block.getFieldValue("AMOUNT"))
		} },
	//Move arm to pre-defined position
	'move_arm_pre':{ id:'move_arm_pre',output:function(block){ 
			return RBLOCKS.createcommand("MOVEARM","DEFPOS",block.getFieldValue("POSNAME"))
		} },
	//Move the arm to a valid random position
	'move_arm_random':{ id:'move_arm_random',output:function(block){ 
			return RBLOCKS.createcommand("MOVEARM","RANDOM","")
		} },
	//Toggle gripper status
	'gripper_status':{ id:'gripper_status',output:function(block){  
			return RBLOCKS.createcommand("GRIPPER","SET",block.getFieldValue("GRIPPER_STATUS"))
		} },
	//Gripper state condition
	'gripper_state_cond':{ id:'gripper_state_cond',output:function(block){  
			return RBLOCKS.createcommand("","","")
		} },
	//Wait command
	'wait':{ id:'wait',output:function(block){
			return RBLOCKS.createcommand("UTIL","WAIT",block.getFieldValue("AMOUNT"))
		
		 }},
	//Camera follow command
	'camera_follow':{ id:'camera_follow',output:function(block){
			return RBLOCKS.createcommand("CAMERA","FOLLOW",block.getFieldValue("STATUS"))
		
		 }},	
	
	//Create command structure
	createcommand:function(type,att,val){
		console.log("Sending command values")
		console.log("Type: " + type)
		console.log("Attribute: " + att)
		console.log("Value: " + val)
		return type + "," + att + "," + val
	},
	//Create a vel dependent command
	createVelCommand:function(type,dir,amount){ return RBLOCKS.createcommand(type,dir,amount) }
}
//START ROBOT
////https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#svhneq
Blockly.Blocks[RBLOCKS.start_robot.id] = {
  init: function() {
	this.id = RBLOCKS.start_robot.id
    this.appendDummyInput()
        .appendField("START ROBOT");
    this.setNextStatement(true);
    this.setColour(500);
    this.setTooltip('');
    this.setHelpUrl(HELP_URL);
  }
}; 

//MOVE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#cckrgt
Blockly.Blocks[RBLOCKS.move.id] = {
  init: function() {
	this.id = RBLOCKS.move.id
    this.appendDummyInput()
        .appendField(" MOVE")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"], ["forwards", "FORWARDS"], ["back", "BACK"]]), "DIRECTION")
        .appendField("amount")
        .appendField(new Blockly.FieldTextInput("0"), "AMOUNT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(100);
    this.setTooltip('Move the robot by amount, in specified direction');
    this.setHelpUrl(HELP_URL);
  }
}; 

//ROTATE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#mbz6sk
Blockly.Blocks[RBLOCKS.rotate.id] = {
  init: function() {
    this.id = RBLOCKS.rotate.id
    this.appendDummyInput()
        .appendField("ROTATE")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]), "DIRECTION")
        .appendField("amount")
        .appendField(new Blockly.FieldTextInput("0"), "AMOUNT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(120);
    this.setTooltip('Rotate the robot by amount, in specified direction');
    this.setHelpUrl(HELP_URL);
  }
}; 
 
//ROTATE JOINT
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#n9qvsj
Blockly.Blocks[RBLOCKS.rotate_joint.id] = {
  init: function() {
	this.id = RBLOCKS.rotate_joint.id
    this.appendDummyInput()
        .appendField("ROTATE JOINT")
        .appendField(new Blockly.FieldDropdown([["arm_joint_1", "arm_joint_1"], ["arm_joint_2", "arm_joint_2"], ["arm_joint_3", "arm_joint_3"], ["arm_joint_4", "arm_joint_4"], ["arm_joint_5", "arm_joint_5"]]), "ID")
        .appendField("amount")
        .appendField(new Blockly.FieldTextInput("0"), "AMOUNT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(200);
    this.setTooltip('Rotate specified joint by given joint space value');
    this.setHelpUrl(HELP_URL);
  }
}; 

//MOVE ARM PRE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#j8ting
Blockly.Blocks[RBLOCKS.move_arm_pre.id] = {
  init: function() {
	this.id = RBLOCKS.move_arm_pre.id
    this.appendDummyInput()
        .appendField("MOVE ARM")
        .appendField(new Blockly.FieldTextInput("position name.."), "POSNAME");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('Move arm to pre-defined position (E.G candle,folded)');
    this.setHelpUrl(HELP_URL);
  }
}; 

//MOVE ARM RANDOM
Blockly.Blocks[RBLOCKS.move_arm_random.id] = {
  init: function() {
	this.id = RBLOCKS.move_arm_random.id
    this.appendDummyInput()
        .appendField("MOVE ARM")
	.appendField("RANDOM")
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('Move arm to a random valid position');
    this.setHelpUrl(HELP_URL);
  }
}; 


//GRIPPER STATUS
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#j8ting
Blockly.Blocks[RBLOCKS.gripper_status.id] = {
  init: function() {
	this.id = RBLOCKS.gripper_status.id
    this.appendDummyInput()
        .appendField("GRIPPER")
        .appendField(new Blockly.FieldDropdown([["OPEN", "GRIPPER_OPEN"], ["CLOSE", "GRIPPER_CLOSE"]]), "GRIPPER_STATUS");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(250);
    this.setTooltip('Set gripper status');
    this.setHelpUrl(HELP_URL);
  }
}; 

//IF GRIPPER STATE
//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#aa6qba
Blockly.Blocks[RBLOCKS.gripper_state_cond.id] = {
  init: function() {
	this.id = RBLOCKS.gripper_state_cond.id
    this.appendDummyInput()
        .appendField("IF")
        .appendField("GRIPPER STATE")
        .appendField(new Blockly.FieldDropdown([["CLOSED", "CLOSED"], ["OPEN", "OPEN"]]), "GRIPPER_S")
        .appendField("THEN");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(320);
    this.setTooltip('IF condition - checks gripper state');
    this.setHelpUrl(HELP_URL);
  }
}; 

//WAIT
Blockly.Blocks[RBLOCKS.wait.id] = {
	init: function(){
		this.id = RBLOCKS.wait.id
		this.appendDummyInput()
			.appendField("WAIT")
			.appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"],["3","3"],["4","4"],["5","5"],["6","6"],
			["7","7"],["8","8"],["9","9"],["10","10"]]), "AMOUNT")
			.appendField("SECONDS")
		this.setPreviousStatement(true)
		this.setNextStatement(true)
		this.setColour(330)
		this.setTooltip('Wait for specified time')
		this.setHelpUrl(HELP_URL)
	}
};

//CAMERA FOLLOW
Blockly.Blocks[RBLOCKS.camera_follow.id] = {
  init: function() {
	this.id = RBLOCKS.camera_follow.id
    this.appendDummyInput()
        .appendField("CAMERA FOLLOW")
        .appendField(new Blockly.FieldDropdown([["UTIL_REACHED", "UTIL_REACHED"], ["NO_TIMEOUT", "NO_TIMEOUT"]]), "STATUS")
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(320);
    this.setTooltip('Camera - track, and follow object using Whycon');
    this.setHelpUrl(HELP_URL);
  }
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
		//alert(block.id)
		block.select();
		//var col = block.getColour();
		var id = block.id
		//Push output command
		commands.push(RBLOCKS[id]['output'](block))
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
		//Check the id of the block.. is it a start_robot block?
		if(blocks[i].id==RBLOCKS.start_robot.id){
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

