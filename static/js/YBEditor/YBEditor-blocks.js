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
    this.setColour(0);
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