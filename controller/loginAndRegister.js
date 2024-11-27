const bcrypt = require('bcryptjs');
const { createUserQuery, loginQuery} = require("../model/tasks");
const jwt = require("jsonwebtoken")
require("dotenv").config()

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
        
        const token = jwt.sign(
            { id: user.rows[0].id, username: user.rows[0].username, role: user.rows[0].role },
            process.env.JWT_SECRET_KEY,
            { expiresIn: '1h' }  
        );

        res.cookie('auth_token', token, { httpOnly: true})

        req.session.user = {
            id: user.rows[0].id,
            username: user.rows[0].username,
            role: user.rows[0].role,
            email: user.rows[0].email
        };
        console.log("user created!" , req.session.user)

        return res.status(200).send(user)
        

    } catch(error) {
        res.status(500).send({message:`Could not login : ${error.message}`})
    }
}

const isAuthenticated = (req, res, next) => {
    const token = req.cookies.auth_token || req.headers['authorization'];

    if (!token) {
        return res.status(401).send({ message: 'Unauthorized' });
    }

    jwt.verify(token, process.env.JWT_SECRET_KEY, (err, decoded) => {
        if (err) {
            return res.status(401).send({ message: 'Invalid token' });
        }
        req.user = decoded;  
        return next();  
    });
};

const getSession = (req, res, next) => {
    const token = req.cookies.auth_token || req.headers['authorization']; 
  
    if (!token) {
        console.log("Le token n'est pas trouvé")
        return next(); 
    }
  
    try {
      
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
  
      
      req.session.user = {
        id: decoded.id,
        username: decoded.username,
        role: decoded.role
      };
  
      console.log('Session réinitialisée avec les données du token');
      return next(); 
  
    } catch (error) {
      console.error('Erreur lors de la vérification du token:', error);
      return res.status(401).send('Token invalide ou expiré');
    }
  };

module.exports = { createUser, login, isAuthenticated, getSession }