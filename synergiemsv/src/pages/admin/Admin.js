import React, {useEffect, useContext} from "react";
import { NavLink, useParams } from "react-router-dom";
import { Outlet } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import { useNavigate } from "react-router-dom";
import "../pages.css"



export function Admin() {
    const { user, login} = useContext(AuthContext);
    const { id } = useParams()
  
    const navigate = useNavigate()

    useEffect(() => {
        
        const getUser = async () => {
            try {
                const response = await fetch("http://localhost:3000/api/user", {
                    method: "GET",
                    credentials: 'include'

                })
                if(response.ok){
                    const data = await response.json()
                    login(data)
                    console.log(`récupération des datas : infos de user : ${user}`, data)
                } else {
                    console.error("Failed to fetch user data:", response.statusText);
                }
            } catch(error) {
                console.error("Didn't fetch the user data", error)
            }
        }


        getUser()
    }, [])

    if (!user) {
        // Si les données de l'utilisateur ne sont pas encore chargées, ne pas rediriger
        return <div>Loading...</div>;
      }

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