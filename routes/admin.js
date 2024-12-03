const express = require("express");
const router = express.Router();
const {isAuthenticated} = require("../controller/loginAndRegister");
const { exec } = require('child_process');
const path = require('path');
const {getAdminHomeData} = require("../model/tasks")
const { getAdminHomeDataController, getOverviewDataController, getRoadmapDataController, updateRoadmapTodosController } = require ("../controller/adminController")


router.get("/", getAdminHomeDataController)

router.get("/overview",getOverviewDataController)

router.put("/overview")

router.get("/roadmap", getRoadmapDataController)

router.put("/roadmap", updateRoadmapTodosController )

router.get("/details")

router.put("/details")



/*router.post("/setsession", (req, res) => {
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
})*/


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