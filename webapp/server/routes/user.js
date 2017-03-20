import express from 'express';
import User from '../models/user';
 
const router = express.Router();

// 회원가입 
router.post('/register', (request, response) => {
	let regex = /^[a-zA-Z0-9_]+$/;
	if(!regex.test(request.body.id)) {
		return response.status(400).json({ result: 'invalid-id' }); 
	}

	if(request.body.name.length === 0) {
		return response.status(400).json({ result: 'invalid-name' }); 
	}

	if(request.body.password.length < 4 || request.body.password.length > 12) { 
		return response.status(400).json({ result: 'invalid-password' }); 
	}; 
	
	User.findOne({ id: request.body.id }, (err, exists) => { 
		if(err) { 
			throw err; 
		}; 
		if(exists) { 
			return response.status(409).json({ result: 'duplicated-id' }); 
		}; 
		
		let user = new User({ 
			id: request.body.id, 
			name: request.body.name, 
			gender: request.body.gender || 0, 
			password: request.body.password, 
			email: request.body.email || '', 
			administrator: 0, 
		}); 
		user.password = user.generateHash(user.password); 
	
		user.save(err => { 
			if(err) { 
				throw err; 
			}; 
			return response.json({ result: true }); 
		}); 
	});  
});

// 로그인 
router.post('/login', (request, response) => {
	if(request.body.id.length === 0 || request.body.password.length === 0)  { 
		return response.status(400).json({ code: 1, result: 'argument-error' }); 
	} 
	User.findOne({ id: request.body.id }, (err, user) => { 
		if(err) { 
			throw err; 
		};
		if(!user) { 
			return response.status(401).json({ code: 2, result: 'invalid-user' }); 
		}
		if(!user.validateHash(request.body.password)) { 
			return response.status(401).json({ code: 3, result: 'invalid-password' }); 
		}
		
		var data = { 
			id: user.id, 
			name: user.name, 
			email: user.email, 
			created: user.created, 
			administrator: user.administrator }; 
		request.session.key = data; 

		return response.json({ code: 0, result: data, }); 
	}); 
});
 
// 정보가져오기
router.get('/info', (request, response) => {
	if(!request.session || !request.session.key) {
		return response.status(401).json({ result: 'no-info' });
	}
    	response.json({ result: request.session.key });
});

// 로그아웃
router.post('/logout', (request, response) => {
	request.session.destroy(err => { 
		if(err) 
			throw err; 
	});
	return response.json({ result: true });
});
 
export default router;
