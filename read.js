var fs = require('fs'),
	readline = require('readline'),
	stream = require('stream'),
	mongoose = require('mongoose');
var Schema = mongoose.Schema;
var ObjectId = Schema.ObjectId;
mongoose.connect('mongodb://localhost:28017/testDB');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error'));
db.once('open', function callback(){
	var FreestyleSchema = new Schema({
		machineID: String,
		latitude: Number,
		longitude: Number,
		logs: Array
	});

	var FreestyleMachine = mongoose.model('FreestyleMachine', FreestyleSchema);

	var fm = new FreestyleMachine({machineID:"1", longitude:2, latitude:3, logs:[{'test':'this'}]});
	fm.save(function (err, fm){
		console.log("Error saving " + fm);
	});
	mongoose.connection.close();
	/*
	var instream = fs.createReadStream('outFile.txt');
	var outstream = new stream();
	outstream.readable = true;
	outstream.writable = true;

	var rl = readline.createInterface({input: instream,output: outstream,terminal: false});


	var logData;
	var machineID;
	var machineIDs = {};
	rl.on('line', function(line) {
		console.log(line);
		line = line.replace("\r", "").replace("\n","").split("\t");
		logData = {timeStamp:line[1], sys_log_msg_cd:line[2], sys_log_msg_sub_cd:line[3], sys_log_msg_val1:line[4], sys_log_msg_val2:line[5], sys_log_msg_txt:line[6]};
		machineID = line[0].replace('"',"");
		if(typeof machineIDs[machineID] != 'undefined'){
			FreestyleMachine.update({'machineID': machineID}, {"$push": {logs:logData}});		
		}else{
			machineIDs[machineID] = 1; 
			fm = new FreestyleMachine({ 'machineID':machineID, logs:logData});
			fm.save(function(err, fsm){
				if(err) return console.error("Error while saving data to MongoDB: " + err); // <- this gets executed when there's an error
				console.error(fsm);
			});
		}
	});
	mongoose.connection.close();
	*/
});

