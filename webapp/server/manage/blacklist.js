const http = require('http');
const express = require('express');
const router = express.Router();

const fetcher = require('../modules/fetcher'); 

// 블랙리스트 조회
router.get('/', (request, response) => {
	fetcher.pyscript('blacklist.py', 'r ALL', (err, stdout, stderr) => { 
		response.json(err ? { status: false, error: err, data: stderr } : JSON.parse(decodeURIComponent(stdout))); 
	}); 
});
router.get('/search/:name', (request, response) => { 
	fetcher.pyscript('blacklist.py', 'r ' + encodeURIComponent(request.params.name), (err, stdout, stderr) => { 
		response.json(err ? { status: false, error: err, data: stderr } : JSON.parse(decodeURIComponent(stdout))); 
	}); 
}); 
router.get('/access/:ids', (request, response) => { 
	fetcher.pyscript('blacklist.py', 'rr ' + request.params.ids, (err, stdout, stderr) => { 
		response.json(err ? { status: false, error: err, data: stderr } : JSON.parse(decodeURIComponent(stdout))); 
	}); 
}); 
router.get('/count', (request, response) => { 
	fetcher.pyscript('blacklist.py', 'rc stats' + encodeURIComponent(request.params.name), (err, stdout, stderr) => { 
		response.json(err ? { status: false, error: err, data: stderr } : JSON.parse(decodeURIComponent(stdout))); 
	}); 
}); 

// 블랙리스트 등록
router.post('/', (request, response) => { 
	let type = request.body.type; 
	let name = request.body.name; 
	if(type && name) { 
		fetcher.pyscript('blacklist.py', 'c ' + type + ':' + encodeURIComponent(name), (err, stdout, stderr) => { 
			response.json(err ? { status: false, error: err, data: stderr } : JSON.parse(decodeURIComponent(stdout))); 
		}); 
	} 
	else { 
		response.json({ status: false, error: 'params error', data: null }); 
	}; 
}); 

// 블랙리스트 삭제 
router.post('/delete', (request, response) => { 
	let id = request.body.id; 
	if(id) { 
		fetcher.pyscript('blacklist.py', 'd ' + id, (err, stdout, stderr) => { 
			response.json(err ? { status: false, error: err, data: stderr } : JSON.parse(decodeURIComponent(stdout))); 
		}); 
	} 
	else { 
		response.json({ status: false, error: 'params error', data: null }); 
	}; 
}); 

// 블랙리스트 강제
router.post('/update', (request, response) => { 
	let id = request.body.id; 
	if(id) { 
		fetcher.pyscript('blacklist.py', 'u ' + id, (err, stdout, stderr) => { 
			response.json(err ? { status: false, error: err, data: stderr } : JSON.parse(decodeURIComponent(stdout))); 
		}); 
	} 
	else { 
		response.json({ status: false, error: 'params error', data: null }); 
	}; 
}); 
module.exports = router;
