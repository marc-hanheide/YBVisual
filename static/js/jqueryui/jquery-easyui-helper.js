/**

	Contains helper classes for use with JQUERY EASYUI

**/



//Creates a basic div component
function SimpleDiv(_id,_width,_height,_class,_parent){
	//Create the DIV components
	var div = $('<div/>',
	{
		id:_id,
		class: _class
	}).appendTo(_parent);
	//Now set the dimensions of the main DIV components
	div.width(_width);
	div.height(_height);
	//The component needs a border
	div.css({"border-color": "#C1E0FF", 
             "border-width":"1px", 
             "border-style":"solid"});
	//Return the resulting div
	return div;
}
//Create a complex div component, for this component - content may be appended
function ComplexDiv(_id,_width,_height,_class,_parent,_append){
	//First, create a simple div
	var div = SimpleDiv(_id,_width,_height,_class,_parent);
	//Now add the appended contents
	div.append(_append);
	//Now return the  div
	return div;
	
}

//Creates a basic draggable div with the specified title and dimensions
function SimpleDraggableDiv(_id,_width,_height,_parent){
	//Create the div and make it draggable
	return SimpleDiv(_id,_width,_height,'easyui-draggable',_parent).draggable();
}
//Create a draggable div with a title div
function DraggableDiv(_id,_title,_width,_height,_parent){
	//Create the initial draggable div
	var _draggable = SimpleDraggableDiv(_id,_width,_height,_parent);
	/*
		Now create the title div, and set the draggable div as its parent
	*/
	_draggable.append( "<div>" +  _title + "</div>" );
	
	//Return the div
	return _draggable;
	
}


//Used to create a combo box
function ComboBox(atts,_class,_parent){
	
	
	var _select = $('</select>');
	
	$(atts).each(function()
	{
		_select.append($("<option>").attr('value',this.val).text(this.text));
	});
	
	_select.addClass(_class);
	
	//Now return the combobox
	return _select;
	
}


//Create a draggable div containing a combo, and value box
function DraggableDiv_Select(_id,_title,_width,_height,_parent,_atts){
		
		//Create a draggable  div
		var _div = DraggableDiv(_id,_title,_width,_height,_parent);
		
		var _options = ComboBox(_atts,'easyui-combobox',_div);
		_div.append(_options);
		
		
		//We can return the resulting div
		return _div;
}







