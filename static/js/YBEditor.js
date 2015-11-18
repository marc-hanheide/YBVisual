/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */



/*
 *  This struct is used to hold information regarding information such as:
 *  ROBOT IP - The IP of the connected robot
 *  CONNECTION STATUS - Is the robot connected correctly?
 *  
 *  
 *  
 *  Also functions:
 *  Connect - Connect to the robot with the specified ip
 */
var SESSION =  {
    /*
     * Information/Variables
     */
    //Holds robot connection information
    'CONNECTION_INFO':
     {
         /* VARIABLES */
       'ip':null, //IP address
       'port':null, //Port
       'status':false //Connection status - initially false
     },
     //Holds information regarding the currently opened project
     'PROJECT':
     {
         /* VARIABLES */
        'filename':null, //The filename used by the project
        'commands':
                {
                    /* VARIABLES */
                    list:[], //The list containing the commands
                    
                    /* FUNCTIONS */
                    Add:function(divid,cmdtype)
                    {
                        console.log("Adding command..");
                        
                        //We need to find the id for the new command
                        id = 0;
                        //Is there any commands?, if not - ID is 1
                        if(list.length === 0){ id = 1; }
                        //Else calculate a unique ID
                        else
                        {
                            //Temp
                            _id = 0;
                           //Cycle through and check for the highest id
                           for (i = 0;i < list.length; i++){
                               //If higher - replace
                               if(list[i].id > _id){ id = list[i].id; }else{ }
                           }
                           _id + _id + 1;
                           //This is the new id
                           id = _id;
                       }
                       /* --- We now have the ID for the new command -- */
                       //Add the command to the array depending on the given type, and divid
                       list.push(new Command(id,divid,cmdtype));
                       
                       //Log
                       console.log("Command added");
                   },
                   Remove:function(id)
                   {
                       //Log
                       console.log("Removing command");
                       //Was the command found
                       found = false;
                       
                       //Find the element using the given id
                       for(i  =0; i < list.length;i++)
                       {
                           //Found
                           if(list[i].id === id)
                           {
                               found = true;
                               
                               //Now remove
                               list.splice(i,1);
                           }
                               
                       }
                       
                       //Log whether command was found, and removed
                       if(found){ console.log("Command found, and removed"); }
                       else{ console.log("Command with id: " + id + " not found"); }
                   }
               }, //The current commands controlling the robot
        
        /* FUNCTIONS */
        //Start a new project
        'New':function()
        {
            //Log
            console.log("Starting new project..");
            
        },
        //Open an existing project
        'Open':function()
        {
            //Log
            console.log("Opening existing project..");
        },
        //Save the currently opened project to file
        'Save':function()
        {
            //Log
            console.log("Saving the project..");
            
        }
     },
    
    /*
     * Functions
     */
    'Connect':function(ip,port)
    {
        //Log connection attempt
        console.log("Attempting to connect to robot on IP: " + ip + " and port: " + port);
        
        
        /*
         * Log connection success
         */
        console.log("Connected.");
        console.log("Connected IP: " + ip);
        console.log("Connected port: " + port);
        /*
         * Set connection info
         */
        SESSION.CONNECTION_INFO.ip = ip; //Set connection IP
        SESSION.CONNECTION_INFO.port = port; //Set connection port
        SESSION.CONNECTION_INFO.status = true; //Set connection status
    }
    
    
            
};


/*
 * Class define different command types
 */
//Primary command class
function Command(id,divid,cmdtype)
{
    this.id = id; //The ID of this command
    this.divid = divid; //The ID of the div using this command
    this.cmdtype = cmdtype; //The type of this command
}

//Move forward command
function Move_Foward(amount){ this.type = "move"; this.amount = amount; };
//Move back command
function Move_Back(amount){ this.type = "move"; this.amount = amount; };
//Move left command
function Move_Left(amount){ this.type = "move"; this.amount = amount; };
//Move right command
function Move_Right(amount){ this.type = "move"; this.amount = amount; };
