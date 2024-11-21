require('dotenv').config();
const express = require('express');
const app = express();
const PORT = 3000;
const crypto = require("crypto");
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const { URLSearchParams } = require("url");
const {template} = require("./canvaTemplate");
const adminRoute = require("../routes/admin");
const registerRoute = require("../routes/register");
const loginRoute = require("../routes/login")
const cors = require('cors');
app.use(cors()); 



const codeVerifier = crypto.randomBytes(96).toString("base64url");
const codeChallenge = crypto
  .createHash("sha256")
  .update(codeVerifier)
  .digest("base64url");




const clientId = process.env.CANVA_CLIENTID;
const clientSecret = process.env.CANVA_SECRETID;
const authURL = process.env.CANVA_AUTHURL + codeChallenge;
const redirectURI = "http://127.0.0.1:3000/callback/";
let accessToken = "";
let refreshToken = "";

app.use("/admin", adminRoute)
app.use("api/register", registerRoute)
app.use("/login", loginRoute)
app.use(cors()); 

app.get("/", (req,res) => {
    
})

app.get("/callback", async (req,res) => {
    const authCode = req.query.code;
    if(authCode) {
        try{
        const credentials = `${clientId}:${clientSecret}`;
        const base64Credentials = Buffer.from(credentials).toString('base64');
        const response = await fetch("https://api.canva.com/rest/v1/oauth/token", {
            method: "POST",
            headers: {
              "Authorization": `Basic ${base64Credentials}`,
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                grant_type: "authorization_code",
                code_verifier: codeVerifier,
                code: authCode, 
                redirect_uri: redirectURI
            })
        });
        const data = await response.json();
        accessToken = await data.access_token;
        refreshToken = await data.refresh_token;
        console.log(data);    
        res.status(200).json(data);
        template(accessToken, refreshToken);
        
        
      } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching token");
      }
    } else {
      res.status(404).send("Could not get code");
    }

});






app.listen(PORT, () =>{
    console.log(`Listening to port : ${PORT}`)
})

module.exports = {
    accessToken : accessToken,
    refreshToken : refreshToken
}