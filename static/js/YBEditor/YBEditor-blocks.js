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
    this.setColour(400);
    this.setTooltip('');
    this.setHelpUrl(HELP_URL);
  }
};
//Python code
Blockly.Python[RBLOCKS.start_robot.id] = function(block) {
	var code =  "";
	return [code,Blockly.Python.ORDER_ATOMIC]
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
    this.setColour(120);
    this.setTooltip('Move the robot by amount, in specified direction');
    this.setHelpUrl(HELP_URL);
  }
};
//Python code
Blockly.Python[RBLOCKS.move.id] = function(block) {
  var dir = block.getFieldValue('DIRECTION');
  var amount = block.getFieldValue('AMOUNT');
  // TODO: Assemble Python into code variable. 
  var amountf = parseFloat(amount)
  code = "self.robot.DriveDirection(" + "'" +  dir + "'" + "," + amountf + ")"
  code = code + " \n"
  return code;
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
    this.setColour(130);
    this.setTooltip('Rotate the robot by amount, in specified direction');
    this.setHelpUrl(HELP_URL);
  }
}; 
//Python code
Blockly.Python[RBLOCKS.rotate.id] = function(block){
	var dir = block.getFieldValue('DIRECTION')
	var amount = block.getFieldValue('AMOUNT')
	var amountf = parseFloat(amount)
	code = "self.robot.RotateDirection(" + "'" +  dir + "'" + "," + amountf + ")"
	code = code + "\n"
	return code;
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
    this.setColour(140);
    this.setTooltip('Move arm to pre-defined position (E.G candle,folded)');
    this.setHelpUrl(HELP_URL);
  }
}; 
//Python code
Blockly.Python[RBLOCKS.move_arm_pre.id] = function(block){
	var pos = block.getFieldValue('POSNAME')
	code = "self.robot.Reach('" + pos + "')\n"
	return code;
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
    this.setColour(150);
    this.setTooltip('Move arm to a random valid position');
    this.setHelpUrl(HELP_URL);
  }
}; 
//Python code
Blockly.Python[RBLOCKS.move_arm_random.id] = function(block){
	code = "self.robot.Reach('random')\n"
	return code;
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
//Python code
Blockly.Python[RBLOCKS.gripper_status.id] = function(block){
	var status = block.getFieldValue('GRIPPER_STATUS')
	code = ""
	if(status==="GRIPPER_OPEN"){ code = "self.robot.Drop()"  }else{ code ="self.robot.Grab()" }
	code = code + "\n"
	return code;
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
		this.setColour(180)
		this.setTooltip('Wait for specified time')
		this.setHelpUrl(HELP_URL)
	}
};
//Python code
Blockly.Python[RBLOCKS.wait.id] = function(block){ var amountf = parseFloat(block.getFieldValue('AMOUNT')); return "self.robot.Pause(" + amountf + ")\n"; }

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



