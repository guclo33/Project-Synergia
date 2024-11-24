import React, {useState, useEffect} from "react";
import image from "../../Images/logo2 sans fond.png"
import { LoginForm } from "./components/LoginForm";
import { useNavigate } from "react-router";
import { Link } from "react-router-dom";

export function Login() {
    const [userData, setUserData] = useState({
        usernameOrEmail : "",
        password : ""
    })
    const [verified, setVerified] = useState(false);

    const navigate = useNavigate()

    useEffect(() => {
        if(userData.usernameOrEmail.length > 0 && userData.password.length > 0){
            setVerified(true)
        }
    }, [userData])
    
    const handleChange = (e) => {
        const {name, value} = e.target
        setUserData((prev) =>({
            ...prev,
            [name] : value
        }))
    }

    const handleSubmit= async (e) => {
        e.preventDefault()
        if (verified){
            try {
                const response = await fetch("http://10.0.0.6:3000/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        usernameOrEmail : userData.usernameOrEmail,
                        password: userData.password
                    })
                });
                if(response.ok){
                    const existingUser = await response.json();
                    console.log(`User succesfully match with role : ${existingUser.rows[0].role}`)
                    navigate(`/${existingUser.rows[0].role}`)

                } else {
                    const errorData = await response.json()
                    console.log("error", errorData.message)
                    alert(`Error : ${errorData.message}`)
                }


            } catch(error){
                console.log("user not found")
                alert("Couldn't get user, have you created your account?")
            }
        } else {
            alert("Les champs sont vide!")
        }
    }
    
    return(
        <>
            <nav>
                <ul>
                    <li><a href="https://www.synergiemsv.com">Synergie MSV</a></li>
                    <li><Link to="/">Accueil</Link></li>
                    <li><Link to="/login">Se connecter</Link></li>
                    <li><Link to="/register">Créer un compte</Link></li>
                </ul>
            </nav>
            <div className="login">
                <img src={image} alt="logo SynergieMSV" />
                <LoginForm handleSubmit={handleSubmit} handleChange={handleChange} userData={userData}/>
                
            </div>
        </>
    )
}