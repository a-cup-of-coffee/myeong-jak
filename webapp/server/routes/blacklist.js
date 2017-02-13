const express = require('express');  
const router = express.Router();

const fetcher = require('../modules/fetcher'); 

router.get('/:id', (req, res) => {
	fetcher.pyscript('blacklist/blacklist.py', 'r ' + req.params.id, function(err, result) { 
		return res.json({
			error: err,  
			result: result, 
		});
	}); 
});

module.exports = router; 
