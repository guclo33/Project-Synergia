const express = require('express');
const app = express();
const PORT = 3000;
const {connectCanva} = require("./canvaTemplate");
const adminRoute = require("../routes/admin");
const registerRoute = require("../routes/register");
const loginRoute = require("../routes/login")
const cors = require('cors');


app.use(cors()); 
app.use(express.json());
app.use(cors()); 

//app.use("/api/admin", adminRoute)
app.use("/api/register", registerRoute)
app.use("/api/login", loginRoute)




app.get("/callback", connectCanva);


app.listen(PORT, "0.0.0.0", () =>{
    console.log(`Listening to port : ${PORT}`)
})

