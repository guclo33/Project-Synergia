const express = require('express');
const app = express();
const session = require('express-session');
const PORT = 3000;
const {connectCanva, getAuthUrl}} = require("./canvaTemplate");
const adminRoute = require("../routes/admin");
const registerRoute = require("../routes/register");
const loginRoute = require("../routes/login")
const cors = require('cors');
require("dotenv").config()


const allowedOrigins = ['http://10.0.0.6:3001', 'http://localhost:3000', "http://localhost:3001", "https://app-aagr4xe5mic.canva-apps.com", "http://127.0.0.1:3001" ]; // Ajouter ici toutes les origines autorisées

const corsOptions = {
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true); // Autoriser les requêtes
    } else {
      callback(new Error('Not allowed by CORS')); // Bloquer les autres origines
    }
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE'], // Spécifiez les méthodes autorisées
  credentials: true // Si vous utilisez des cookies avec des sessions, autorisez les cookies
};


app.use(express.json());
app.use(session({
    secret: process.env.COOKIE_SECRET_KEY,  
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }  
}));
app.use(cors(corsOptions));

app.use("/api/admin", adminRoute)
app.use("/api/register", registerRoute)
app.use("/api/login", loginRoute)

app.get("/api/canva/authurl/:id", (req,res) => {
  const authURL = getAuthUrl();
  res.json({authURL})
})


app.get("http://127.0.0.1:3000/api/canva/auth", connectCanva);


app.listen(PORT, "0.0.0.0", () =>{
    console.log(`Listening to port : ${PORT}`)
})

