import React, {useEffect, useState} from "react";
import { useParams, useLocation } from "react-router";

export function ProfilGenerator() {
    cont [canvaAuth, setCanvaAuth] = useState(false)
    
    const {id} = useParams()
    const location = useLocation

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const code = params.get('code');
        if(code) {
            setCanvaAuth(true)
        }

    }, [location])
    
    const handleCanva = () =>{

    }
    

    return(
        <div className="profilGenerator">
            <h2>Générateur de texte</h2>
            {canvaAuth ?
            <button onClick={handleCanva}>Connect Canva</button> :
            <div>
                <input type="text" value="" name="prénom" />
                <input type="text" value="" name="nom" />
                <button>Générer le profil</button>
            </div>
            }
        </div>
    )
}