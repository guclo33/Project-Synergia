import React, {useEffect, useContext} from "react";
import { NavLink, useParams } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import { Navigate } from "react-router-dom";
import "../pages.css"



export function Admin() {
    const { user } = useContext(AuthContext);
    const { id } = useParams()
  useEffect(() => {
    console.log(user)
    if (!user ) {
      <Navigate to="/login" />;
    }
    if(user.role !== "admin"){
        alert("You don't have the role to be authorized");
        <Navigate to="/unauthorized" />
    }
    if(user.id !== parseInt(id)){
        alert("You don't have the right id to be authorized");
        <Navigate to="/unauthorized" />
    }
  }, [user, id]);

    return(
        <div className="admin">
            <nav className="navAdmin">
                <ul>
                    <li><a href="https://www.synergiemsv.com">Synergie MSV</a></li>
                    <li><NavLink to={`/admin/${id}`} className={({ isActive }) => (isActive ? 'isActive' : '')} exact>Accueil</NavLink></li>
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