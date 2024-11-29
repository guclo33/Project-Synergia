const pool = require("./database");

const createUserQuery = (userName, password, email) => {
    return pool.query("INSERT INTO users (username, password, email) VALUES ($1, $2, $3) RETURNING id", [userName, password, email] )
}

const loginQuery = (userNameOrEmail) =>  {
    
    
    return pool.query("SELECT id, role, password, username, email FROM users WHERE (email = $1 OR username = $1)", [userNameOrEmail]);

    
}

const getAdminData = (userId) => {
    return pool.query("")
}

const findUserById = async (id) => {
    // Remplacez par une requête SQL ou une autre méthode pour récupérer l'utilisateur par ID
    return await database.query('SELECT * FROM users WHERE id = $1', [id]);
};

module.exports = {createUserQuery, loginQuery, findUserById}