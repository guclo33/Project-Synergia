const express = require('express');
const app = express();
const session = require('express-session');
const PORT = 3000;
const {connectCanva} = require("./canvaTemplate");
const adminRoute = require("../routes/admin");
const registerRoute = require("../routes/register");
const loginRoute = require("../routes/login")
const cors = require('cors');
require("dotenv").config()


const allowedOrigins = ['http://10.0.0.6:3001', 'http://localhost:3000']; // Ajouter ici toutes les origines autorisées

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




app.get("/callback", connectCanva);


app.listen(PORT, "0.0.0.0", () =>{
    console.log(`Listening to port : ${PORT}`)
})

