const pool = require("./database");

const createUserQuery = async (userName, password, email) => {
    return await pool.query("INSERT INTO users (username, password, email) VALUES ($1, $2, $3) RETURNING id", [userName, password, email] )
}

const loginQuery = async (userNameOrEmail) =>  {
    return await pool.query("SELECT id, role, password, username, email FROM users WHERE (email = $1 OR username = $1)", [userNameOrEmail]);
}

const getAdminHomeData = async () => {
    return await pool.query("SELECT l.id as leaderid, l.client_id as clientid, l.active as active, c.nom_client as nom, c.email as email, c.phone as phone FROM leader l JOIN client c ON l.client_id = c.id" )
}

const updateInfo = async (table, column, value) => {
    return await pool.query("ALTER TABLE $1 SET $2 = $3", [table, column, value]) // À TRAVAILLER!! NE PEUT PAS METTRE $1 POUR TABLE ET COLUMN
}

const findUserById = async (id) => {
    // Remplacez par une requête SQL ou une autre méthode pour récupérer l'utilisateur par ID
    return await pool.query('SELECT * FROM users WHERE id = $1', [id]);
};

const getOverviewData = async () => {
    return await pool.query("SELECT c.nom_client as nom, l.leader_id, l.date_presentation, l.echeance, l.statut, l.priorite FROM client c JOIN leader ON c.id = leader.client_id JOIN leader_todo l ON leader.id = l.leader_id")
}

const getRoadmapData = async () => {
    return await pool.query("SELECT c.nom_client as nom, l.leader_id, l.creation_messenger, l.date_confirme, l.questionnaire_envoye, l.creation_zoom, l.envoie_factures, l.recept_paiement, l.comptabilite, l.redaction_profil, l.profil_leader, l.pret_partage, l.powerpoint, l.mentimeter, l.planif_rencontres1, l.envoie_introspection, l.rencontres1, l.planif_rencontres2, l.envoie_questionnaire_objectifs, l.rencontres2, l.leader_profil_autres, l.leader_adapter, l.leader_suivi FROM client c JOIN leader ON c.id = leader.client_id JOIN leader_todo l ON leader.id = l.leader_id;")
}

const updateRoadmapTodos = async(query, value, leaderid)=> {
    return await pool.query(query, [value, leaderid])
}


module.exports = {createUserQuery, loginQuery, findUserById, getAdminHomeData, getOverviewData, getRoadmapData, updateRoadmapTodos}