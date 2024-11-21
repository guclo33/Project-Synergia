import React from "react";
import { Link } from 'react-router-dom';
import image from "../../Images/logo2 sans fond.png"



export function Home() {
    return (
        <div className="home">
            <nav>
                <ul>
                    <li><a href="https://www.synergiemsv.com">Synergie MSV</a></li>
                    <li><Link to="/login">Se connecter</Link></li>
                    <li><Link to="/register">Créer un compte</Link></li>
                </ul>
            </nav>
            <img src={image} alt="logo SynergieMSV" />
        </div>
    )
}