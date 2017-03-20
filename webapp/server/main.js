import express from 'express';
import path from 'path';
import WebpackDevServer from 'webpack-dev-server';
import webpack from 'webpack';
import morgan from 'morgan'; 
import bodyParser from 'body-parser'; 
import cookieParser from 'cookie-parser'; 
import mongoose from 'mongoose';
import session from 'express-session';
 
import routes from './routes';

const redis = require('redis');
const redisClient = redis.createClient();
const redisStore = require('connect-redis')(session);

const rfs = require('rotating-file-stream'); 

const app = express();
const port = 3000;
const devPort = 4000; 

const db = mongoose.connection;
db.on('error', console.error);
db.once('open', () => { console.log('Connected to mongodb server'); });
mongoose.connect('mongodb://localhost:27017/acupofcoffee');
 
const logDirectory = path.join(__dirname, '..', 'logs');

var accessLogStream = rfs('acuopofcoffee.log', {
	interval: '1d',
	path: logDirectory
}); 

app.use(morgan('combined', {stream: accessLogStream}));
app.use(session({
	secret: 'acupofcoffee',
	resave: false,
	saveUninitialized: false, 
	store: new redisStore({ host: 'localhost', port: 6379, client: redisClient, ttl: 600 }),
}));
app.use('/', express.static(path.join(__dirname, './../public')));

app.use(cookieParser('secretSign#143_!223'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use('/api', routes);
app.use(function(err, request, response, next) {
	console.error(err.stack);
	response.status(500).send('(_ _)');
});

app.listen(port, () => {
	console.log('Express is listening on port', port);
});

if(process.env.NODE_ENV == 'development') {
	console.log('Server is running on development mode');
	const config = require('../webpack.dev.config');
	const compiler = webpack(config);
	const devServer = new WebpackDevServer(compiler, config.devServer);
	devServer.listen(devPort, () => {
		console.log('webpack-dev-server is listening on port', devPort);
	});
}
