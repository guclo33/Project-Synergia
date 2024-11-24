const bcrypt = require('bcryptjs');
const { createUserQuery, loginQuery} = require("../model/tasks");

const createUser = async (req, res) => {
    try {
        const {username, password, email} = req.body;

        const existingUser = await loginQuery(email);

        if(existingUser.rows.length > 0){
            res.status(400).send({message :"User already exist"})
            return
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        await createUserQuery(username, hashedPassword, email)
        res.status(201).send({message :"User created successfully!"})


    } catch (error) {
         res.status(500).send({message:`Could not create user: ${error.message}`})
    }
};

const login = async (req, res) => {
    const { usernameOrEmail, password} = req.body ;
    console.log(req.body)
    try {
        const existingUser = await loginQuery(usernameOrEmail);
        console.log(existingUser)
        if(existingUser.rows.length <= 0){
            return res.status(400).send({message:"Could not find any matching username or email"})
            
        };

        const isMatch = await bcrypt.compare(password, existingUser.rows[0].password)
        if (!isMatch) {
            return res.status(400).send({ message: "Password not matching" });
        }
        if(isMatch) {
            

            return res.status(200).send(existingUser)
        } else {
            return res.status(400).send({message:"Password not matching"})
        }

    } catch(error) {
        res.status(500).send({message:`Could not login : ${error.message}`})
    }
}

module.exports = { createUser, login }