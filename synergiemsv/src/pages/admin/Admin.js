import React, {useEffect, useContext} from "react";
import { NavLink, useParams } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";
import "../pages.css"



export function Admin() {
    const { user } = useContext(AuthContext);
    const { id } = useParams()
  
    const navigate = useNavigate()

    if(user.role !== "admin" && user.id !== id) {
            navigate("/unauthorized");
            return null;
        }

    return(
        <div className="admin">
            <nav className="navAdmin">
                <ul>
                    <li><a href="https://www.synergiemsv.com">Synergie MSV</a></li>
                    <li><NavLink to={`/admin/${id}`} className={({ isActive }) => (isActive ? 'isActive' : '')} >Accueil</NavLink></li>
                    <li><NavLink to="overview" className={({ isActive }) => (isActive ? 'isActive' : '')} >Vue d'ensemble</NavLink></li>
                    <li><NavLink to="roadmap" className={({ isActive }) => (isActive ? 'isActive' : '')} >Feuille de route</NavLink></li>
                    <li><NavLink to="details" className={({ isActive }) => (isActive ? 'isActive' : '')} >Informations</NavLink></li>
                    <li><NavLink to="settings" className={({ isActive }) => (isActive ? 'isActive' : '')} >Paramètres</NavLink></li>
                </ul> 
            </nav>
            <h1>Bienvenue {user.username}</h1>
            <Outlet />
        </div>
    )
}