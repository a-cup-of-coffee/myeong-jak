var http = require('http');
var express = require('express');
var router = express.Router();

router.get('/', (request, response) => {
	response.json({ 'ok': 'ok' }); 
});
module.exports = router;
