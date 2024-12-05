const {getAdminHomeData, getOverviewData, getRoadmapData, updateRoadmapTodos, updateOverview, getDetailsData} = require("../model/tasks")

const getAdminHomeDataController = async (req,res) => {
    try {
        const data = await getAdminHomeData()
        
        if(data){
            
            return  res.status(200).send(data)
        }
        res.send(404).send("no data found")
        return
    } catch (error){
        return res.send(500).send("internal server error")
    }
};

const getOverviewDataController = async (req, res) =>{
    try {
        const data = await getOverviewData()
        
        if(data){
            
            return  res.status(200).send(data)
        }
        res.send(404).send("no data found")
        return
    } catch (error){
        return res.send(500).send("internal server error")
    }
};

const getRoadmapDataController = async (req, res) =>{
    
    try {
        const data = await getRoadmapData()
        
        if(data){
            
            return  res.status(200).send(data)
        }
        res.status(404).send("no data found")
        return
    } catch (error){
        console.log("erreur getRoadmap")
        return res.status(500).send("internal server error")
    }
}

const updateRoadmapTodosController = async (req, res) => {
    const {value, name, leaderid} = req.body
    
    if (value === undefined || !name || !leaderid) {
        return res.status(400).send("Missing parameters");
    }
    let column = ""
    
    switch (name) {
        case "Création du groupe messenger": column = "creation_messenger"; break;
        case "Date confirmé": column = "date_confirme"; break;
        case "Questionnaires et Consignes envoyés": column = "questionnaire_envoye"; break;
        case "Création Zoom": column = "creation_zoom"; break;
        case "Envoie des factures": column = "envoie_factures"; break;
        case "Comptabilité à jour": column = "comptabilite"; break;
        case "Rédaction profiles": column = "redaction_profil"; break;
        case "Profile Leader": column = "profil_leader"; break;
        case "Tout importer, prêt à partagé": column = "pret_partage"; break;
        case "Présentation powerpoint": column = "powerpoint"; break;
        case "Mentimeter": column = "mentimeter"; break;
        case "Planification des rencontres 1": column = "planif_rencontres1"; break;
        case "Envoie du questionnaire Introspection": column = "envoie_introspection"; break;
        case "Rencontres 1": column = "rencontres1"; break;
        case "Planification des rencontres 2": column = "planif_rencontres2"; break;
        case "Envoie des questionnaires objectifs": column = "envoie_questionnaire_objectifs"; break;
        case "Rencontre 2": column = "rencontres2"; break;
        case "Rencontre leader, profiles des autres": column = "leader_profil_autres"; break;
        case "Rencontre leader, S'adapter": column = "leader_adapter"; break;
        case "Rencontre leader, Suivi": column = "row.leader_suivi"; break;
        default: column = name

    };
    const query = `UPDATE leader_todo SET ${column} = $1 WHERE leader_id = $2`

    try {
        await updateRoadmapTodos(query, value, leaderid)
        res.status(200).send("Succesfully updated todos!")
    } catch(error) {
        res.status(400).send(error)
    }
}

const updateOverviewController = async (req, res) => {
    const { leader_id, date_presentation, echeance, statut, priorite} = req.body;
    console.log("req.body=", req.body)
    console.log("leader id", leader_id,"date pres:", date_presentation,"echeance", echeance,'statut', statut,"priorite", priorite)
    try {
        await updateOverview(date_presentation, echeance, statut, priorite, leader_id)
        res.status(200).send("completed update overview")
    } catch(error) {
        res.status(400).send(error)
    }

}

const getDetailsById = async (req,res) => {
    const {clientid} = req.params;
    console.log("clientID:" , clientid)
    try{
        const data = await getDetailsData(clientid)
        console.log(data)
        
        res.status(200).json(data)
    } catch(error) {
        res.status(400).send(error)
    }
}



module.exports = { getAdminHomeDataController, getOverviewDataController, getRoadmapDataController, updateRoadmapTodosController, updateOverviewController, getDetailsById };