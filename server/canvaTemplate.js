const fs = require('fs');
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
const { URLSearchParams } = require("url");
const crypto = require("crypto");
require('dotenv').config();

const codeVerifier = crypto.randomBytes(96).toString("base64url");
const codeChallenge = crypto
  .createHash("sha256")
  .update(codeVerifier)
  .digest("base64url");


const clientId = process.env.CANVA_CLIENTID;
const clientSecret = process.env.CANVA_SECRETID;
const authURL = process.env.CANVA_AUTHURL + codeChallenge;


let accessToken = "";
let refreshToken = "";

const getAuthUrl =() => {
    return authURL
}


const templateDataset = async (templateId, accessToken, refreshToken) => {
    const templateInfos = await fetch(`https://api.canva.com/rest/v1/brand-templates/${templateId}/dataset`,   {
    method: "GET",
    credentials: 'include',
    headers: {"Authorization" : `Bearer ${accessToken}`}
    });
        if (!templateInfos.ok) {
            console.error("Error fetching template information:", templateInfos.status, templateInfos.statusText);
            return;
        }


        const info = await templateInfos.json();
        console.log (info)
        
        await fs.writeFileSync('accessToken.json', JSON.stringify({ accessToken: accessToken, refreshToken: refreshToken, templateId : templateId }));
        return info
        
    }; 


const template = async (accessToken, refreshToken) => {
    let templateId = ""
    if (!accessToken) {
        console.error("Access token is undefined or missing.");
        return;
    }
    try {
        
        const getTemplateId = await fetch("https://api.canva.com/rest/v1/brand-templates",
            {
                method: "GET",
                headers : {
                    "Authorization" : `Bearer ${accessToken}`
                },
                credentials: 'include',
            }
        );
        const templateIdInfos = await getTemplateId.json()
        templateId = await templateIdInfos.items[0].id;
        console.log(templateIdInfos);
        
        try {
            await templateDataset(templateId, accessToken, refreshToken);
        } catch (err) {
            console.log("Could not get template dataset", err)
        }
        

    } catch(err) {
        console.log("Could not get template id", err)
    }
     
}

const connectCanva = async (req,res, next) => {
    const authCode = req.query.code;
    
    const redirectURL = req.session.redirectURL;
    const redirectURI = "http://127.0.0.1:3000/api/canva/auth";
     

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
            credentials: 'include',
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
        console.log(redirectURL) 

        await template(accessToken, refreshToken);

        res.send(data)
        next()
    
        
        
      } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching token");
      }
    } else {
      res.status(404).send("Could not get code");
    }

}





module.exports = {
    connectCanva,
    getAuthUrl
}

