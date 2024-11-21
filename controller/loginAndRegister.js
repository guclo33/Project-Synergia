const bcrypt = require('bcryptjs');
const { createUserQuery, loginQuery} = require("../model/tasks");

const createUser = async (req, res) => {
    try {
        const {username, password, email} = req.body;

        const existingUser = await loginQuery(email);

        if(existingUser.rows.length > 0){
            res.status(400).send("User already exist")
            return
        }

        hashedPassword = await bcrypt.hash(password, 10);
        await createUserQuery(username, hashedPassword, email)
        res.status(201).send("User created!")


    } catch (error) {
         res.status(400).send(`Could not create user: ${error.message}`)
    }
};

const login = async (req, res) => {
    const { usernameOrEmail, password} = req.body ;
    try {
        const existingUser = await loginQuery(usernameOrEmail);
        if(existingUser.rows.length <= 0){
            return res.status(400).send("Could not find any matching username or email")
            
        };

        const isMatch = await bcrypt.compare(password, existingUser.rows[0].password)

        if(isMatch) {
            role = existingUser.rows[0].role
            return res.status(200).send({role})
        } else {
            return res.status(400).send("Password not matching")
        }

    } catch(error) {
        res.status(500).send(`Could not login : ${error}`)
    }
}

module.exports = { createUser, login }