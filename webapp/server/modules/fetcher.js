const path = require('path'); 
const scriptPath = path.resolve(__dirname, '..', '..', '..', 'scripts', 'blacklist'); 

module.exports = { 
	pyscript: function(pycommand, arg, callback) { 
		let command = [ 
			'/usr/bin/python', 
			path.resolve(scriptPath, pycommand), 
			arg].join(' '); 

		require('child_process').exec(command, function(err, stdout, stderr) {
			callback(err, stdout, stderr); 
		}); 
	}, 
}
