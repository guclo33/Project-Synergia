const express = require("express");
const router = express.Router();
const {isAuthenticated} = require("../controller/loginAndRegister")

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


module.exports = router