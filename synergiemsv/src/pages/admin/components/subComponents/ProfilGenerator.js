import React, {useEffect, useState, useContext} from "react";
import { useParams, useLocation, useNavigate  } from "react-router";
import { AuthContext } from "../../../AuthContext";
import Cookies from 'js-cookie'

export function ProfilGenerator() {
    const [canvaAuth, setCanvaAuth] = useState(false)
    const [authURL, setAuthURL] = useState("")
    const navigate = useNavigate()
    const {id} = useParams()
    const location = useLocation()
    const user = useContext(AuthContext)
    const token = Cookies.get('auth_token');

    useEffect(() =>{
        const fetchAuthUrl= async () =>{
            try{
                const response = await fetch(`http://localhost:3000/api/canva/authurl/`, {
                    methode : "GET",
                    credentials: 'include',
                });
                const data = await response.json()

                //const currentLocation = window.location.pathname + window.location.search
                
                //const authUrlWithState = +`${data.authURL}&state=${encodeURIComponent(currentLocation)}`

                setAuthURL(data.authURL)
            }catch(error){
                console.error("error fetching authurl", error)
        }};

        fetchAuthUrl();
    },[]);

    useEffect(() => {
        
        const redirectURL = `http://localhost:3001/admin/${id}`
        
        const sendURL = async () => {
            try{
                const response = await fetch("http://localhost:3000/api/admin", {
                    method : "POST",
                    credentials: 'include',
                    headers : {
                        "Content-Type" : "application/json"
                        
                    },
                    body : JSON.stringify({URL : redirectURL})
                });
                if (response.ok) {
                    console.log("Successfully sent redirect URL");
                } else {
                    console.log("Error sending redirect URL", response.statusText);
                };
                
            } catch (error) {
                console.error("Could not send redirectURL" , error)
            }
        }

        sendURL();
    },[])

    useEffect(()=> {
        const params = new URLSearchParams(window.location.search);
        const auth = params.get("auth")

        if(auth==="true"){
            setCanvaAuth(true)
        } 
    },[])

    const handleCanva = async (e) =>{
        e.preventDefault();
        const currentURL = window.location.href;  // URL actuelle
        const authURLWithState = `${authURL}&state=${encodeURIComponent(currentURL)}`
        window.location.href = authURLWithState;
    }
    
    if(canvaAuth===false) {
        return (
            <div className="profilGenerator">
                <h2>Générateur de texte</h2>
                <button onClick={handleCanva}>Connect Canva</button>
                
             
            </div>
        )
    }

    return(
        <div className="profilGenerator">
            <h2>Générateur de texte</h2>
                <div>
                    <input type="text" value="" name="prénom" />
                    <input type="text" value="" name="nom" />
                    <button>Générer le profil</button>
                </div>
             
        </div>
    )
}

 /*
        try{
            const response = await fetch(`http://localhost:3000/api/canva/${id}`, {
                method: "GET"
            })
            if(response.ok){
                console.log("successfully authorized with Canva")

            } else {
                const error = await response.json();
                console.log(`Error connecting to api : ${error}`)
            }


        } catch(error){
            console.log("Couldn't connect to Canva")
        }*/