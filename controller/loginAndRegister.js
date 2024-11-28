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
    
    try {
        const user = await loginQuery(usernameOrEmail);
        
        
        if(user.rows.length <= 0){
            return res.status(400).send({message:"Could not find any matching username or email"})
            
        };

        const isMatch = await bcrypt.compare(password, user.rows[0].password)
        if (!isMatch) {
            return res.status(400).send({ message: 'Invalid credentials' });
        }
        
       
        req.session.user = {
            id: user.rows[0].id,
            username: user.rows[0].username,
            role: user.rows[0].role,
            email: user.rows[0].email
        };
        
        console.log("user created!" , req.session.user);

        req.session.save((err) => {
            if (err) {
                console.log('Error saving session', err);
            }
        })

        return res.status(200).send(user)
        

    } catch(error) {
        res.status(500).send({message:`Could not login : ${error.message}`})
    }
}

const isAuthenticated = (req, res, next) => {
    
    
    if (req.session && req.session.user) {
        console.log(req.session.user);
        
        return next(); 
    } else {
        return res.status(401).send({ message: 'Unauthorized' });
    }
};


module.exports = { createUser, login, isAuthenticated};