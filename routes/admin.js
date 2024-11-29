const express = require("express");
const router = express.Router();
const {isAuthenticated} = require("../controller/loginAndRegister");
const { exec } = require('child_process');
const path = require('path');


router.get("/", isAuthenticated, (req, res) => {
    
    
    const { id } = req.params;

    console.log("ID from URL:", id);
    console.log("ID from session:", req.session.user.id);
    if (req.session.user.role === "admin") {
        
        if (req.session.user.id === id) {
            res.status(200).send("Bienvenue à ton tableau de bord !");
        } else {
            
            res.status(403).send({ message: "Vous n'êtes pas autorisé à accéder à ce tableau de bord." });
        }
    } else {
        
        res.status(403).send({ message: "Accès refusé. Vous devez être un admin pour accéder à cette page." });
    }
});



router.post("/setsession", (req, res) => {
    const {user} = req.body;
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3001');
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    console.log(user)
    if(!user) {
        return res.status(400).send("Error getting user info")
    }
    req.session.user = user;  
    req.session.save((err) => {
        if (err) {
            console.error("Error saving session:", err);
        } else {
            console.log("Session saved successfully!");
        }
    });
    console.log(req.session.user)
    return res.status(200).send("User session data saved successfully");
})


router.post("/profilgenerator", (req,res) => {
    const { firstName, lastName} = req.body;
    
    if(!firstName || !lastName) {   
        res.status(400).send("Did not receive profile name")
    } 
    const profilName = `${firstName}, ${lastName}`
    const pythonFile = path.join(__dirname, './../GenerateurTexte/Synergia MLM.py');

    exec(`python "${pythonFile}" "${profilName}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ error: stderr });
        }

        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }

        
        res.json({ message: stdout });
    })

})


module.exports = router