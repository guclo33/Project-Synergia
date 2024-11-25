import React, {useEffect, useContext} from "react";
import { Link, useParams } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import { Navigate } from "react-router-dom";



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
            <nav>
                <ul>
                    <li><a href="https://www.synergiemsv.com">Synergie MSV</a></li>
                    <li><Link to="/:id">Accueil</Link></li>
                    <li><Link to="overview">Vue d'ensemble</Link></li>
                    <li><Link to="roadmap">Feuille de route</Link></li>
                    <li><Link to="details">Informations</Link></li>
                    <li><Link to="settings">Paramètres</Link></li>
                </ul>
                <h1>Bienvenue {user.username}</h1>
            </nav>
            <Outlet />
        </div>
    )
}