const express = require("express");
const router = express.Router();
const {isAuthenticated} = require("../controller/loginAndRegister");
const { spawn } = require('child_process');

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

router.post("/", isAuthenticated, (req, res) => {
    const { URL } = req.body; 
    req.session.redirectURL = URL; 

    
    console.log('Redirect URL received:', req.session.redirectURL);
    
    res.status(200).send({ message: 'Redirect URL stored successfully', redirectURL: req.session.redirectURL });
})

router.post("/setsession", (req, res) => {
    const {user} = req.body;
    if(!user) {
        return res.status(400).send("Error getting user info")
    }
    req.session.user = user
    return res.status(200).send("User session data saved successfully");
})


router.post("/profilgenerator", isAuthenticated, (req,res) => {
    const { firstName, lastName} = req.body.name;
    if(!firstName || !lastName) {   
        res.status(400).send("Did not receive profile name")
    } 
    const profilName = `${firstName}, ${lastName}`

    const pythonProcess = spawn('python3', ['Synergia MLM.py', profilName]);
    let results = ""
    let error = ""

    pythonProcess.stdout.on('data', (data) => {
        results += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
        error += data.toString()
    })

    pythonProcess.on('close', (code) => {
        if(code === 0) {
            res.json({message: results.trim()})
        } else {
            res.status(500).json({error : error.trim})
        }
    })

})


module.exports = router