const pool = require("./database");

const createUserQuery = (userName, password, email) => {
    return pool.query("INSERT INTO users (username, password, email) VALUES ($1, $2, $3) RETURNING id", [userName, password, email] )
}

const loginQuery = (userNameOrEmail) =>  {
    
    
    return pool.query("SELECT id, role, password FROM users WHERE (email = $1 OR username = $1)", [userNameOrEmail]);

    
}

module.exports = {createUserQuery, loginQuery}