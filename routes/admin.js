const express = require("express");
const router = express.Router();
const {isAuthenticated} = require("../controller/loginAndRegister")

router.get("/", isAuthenticated, (req, res) => {
    if(req.session.user.role === "admin"){
        res.status(200).send("Bienvenue à ton tableau de bord!")
    } else {
        res.status(403).send({message: "Vous n'êtes pas autorisé"})
    }
})


module.exports = router