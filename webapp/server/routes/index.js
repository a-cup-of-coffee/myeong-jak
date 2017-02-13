const express = require('express'); 
const blacklist = require('./blacklist'); 

const router = express.Router();
router.use('/blacklist', blacklist);

module.exports = router; 
