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
};

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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};


