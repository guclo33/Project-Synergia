const bcrypt = require('bcryptjs');
const { createUserQuery, loginQuery} = require("../model/tasks");

const createUser = async (req, res) => {
    try {
        const {userName, password, email} = req.body;

        const existingUser = await loginQuery(email);

        if(existingUser.rowslength > 0){
            res.status(400).send("User already exist")
            return
        }

        hashedPassword = await bcrypt.hash(password, 10);
        await createUserQuery(userName, hashedPassword, email)
        res.status(201).send("User created!")


    } catch (error) {
         res.status(400).send(`Could not create user: ${error.message}`)
    }
};

const login = async (req, res) => {

}

module.exports = { createUser }