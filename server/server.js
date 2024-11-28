const express = require('express');
const app = express();
const session = require('express-session');
const PORT = 3000;
const {connectCanva, getAuthUrl, getUser, setAuthStatus} = require("./canvaTemplate");
const adminRoute = require("../routes/admin");
const registerRoute = require("../routes/register");
const loginRoute = require("../routes/login")
const cors = require('cors');
require("dotenv").config();
const Redis = require('ioredis');
const connectRedis = require('connect-redis');
const { isAuthenticated } = require('../controller/loginAndRegister');


const sessionSecret = process.env.COOKIE_SECRET_KEY

const RedisStore = connectRedis(session);
const redisClient = Redis.createClient({
  host: 'localhost',  
  port: 6379
});

const allowedOrigins = ['http://10.0.0.6:3001', 'http://localhost:3000', "http://localhost:3001", "https://app-aagr4xe5mic.canva-apps.com", "http://127.0.0.1:3001", "http://localhost:3001/admin" ]; // Ajouter ici toutes les origines autorisées

const corsOptions = {
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true); // Autoriser les requêtes
    } else {
      callback(new Error('Not allowed by CORS')); 
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true 
};


app.use(express.json());
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: sessionSecret,  
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false, httpOnly: true, maxAge: 1000 * 60 * 60 * 24, sameSite: 'None' }  
}));
app.use(cors(corsOptions));

app.use("/api/admin", adminRoute)
app.use("/api/register", registerRoute)
app.use("/api/login", loginRoute)

app.get("/api/canva/authurl/", (req,res) => {
  const authURL = getAuthUrl();
  res.json({authURL})
})

app.get("/api/user", getUser)

app.get("/api/canva/auth", (req,res,next) => {
  console.log(req.session.user)
  next()
},
connectCanva, /*setAuthStatus*/);


app.listen(PORT, "0.0.0.0", () =>{
    console.log(`Listening to port : ${PORT}`)
})

