var payload = msg.payload //Loading sent data from the prevoius node
var dates = []; // Initializing data list to store dates
var temperatures = []; // Initializing data list to store temperatures

//Iterating through the resultset from the database to create date and temperature list seperately
for(let i = 0 ; i < payload.length ; i++){
    
    var date = payload[i].date.toLocaleDateString('default', { month: 'short' , year: 'numeric' }) // Converting the date time format to month and year i.e 01/02/2022 ==> Feb 2022
    var temp = payload[i]["temperature"]; // assigning temperature value in result set to a temperary variable
    temperatures.push(temp); // appending the temperature value to the temperature list
    dates.push(date) // appending the date value to the date list
    
}
// Creating new payload for output

msg.payload = [{
    "series" : ["Temperature"], // tooltip
    "data": [temperatures], // defining data frame
    "labels": dates // defining variables
    
}];

return msg; // returning msg with the payload as output