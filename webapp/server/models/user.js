import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';
 
const Schema = mongoose.Schema;
 
const User = new Schema({
	id: String, 
	name: String,
	gender: String, 
	password: String,
	email: String, 
	administrator: Number, 
	created: { type: Date, default: Date.now }
});

User.methods.generateHash = function(password) {
	return bcrypt.hashSync(password, 8);
};
 
User.methods.validateHash = function(password) {
	return bcrypt.compareSync(password, this.password);
};
 
export default mongoose.model('user', User);
