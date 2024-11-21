import React from "react";
import image from "../../Images/logo2 sans fond.png"
import { LoginForm } from "./components/LoginForm";
import { Link } from "react-router-dom";

export function Login() {
    const handleSubmit= (e) => {

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
                <LoginForm handleSubmit={handleSubmit} />
                
            </div>
        </>
    )
}