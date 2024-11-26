import React, {useEffect, useState} from "react";
import { useParams, useLocation, useNavigate  } from "react-router";

export function ProfilGenerator() {
    const [canvaAuth, setCanvaAuth] = useState(false)
    const [authURL, setAuthURL] = useState("")
    const navigate = useNavigate()
    const {id} = useParams()
    const location = useLocation()

    useEffect(() =>{
        const fetchAuthUrl= async () =>{
            try{
                const response = await fetch(`http://localhost:3000/api/canva/authurl/${id}`);
                const data = await response.json()
                console.log(data.authURL)
                setAuthURL(data.authURL)
            }catch(error){
                console.error("error fetching authurl", error)
        }};

        fetchAuthUrl();
    },[]);

    const handleCanva = () =>{
        
        window.open("http://127.0.0.1:3000/api/canva/auth", '_blank');
       
    }
    

    return(
        <div className="profilGenerator">
            <h2>Générateur de texte</h2>
            {canvaAuth ? 
            <div>
                <input type="text" value="" name="prénom" />
                <input type="text" value="" name="nom" />
                <button>Générer le profil</button>
            </div>
             :
             <button onClick={handleCanva}>Connect Canva</button>
            
            }
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