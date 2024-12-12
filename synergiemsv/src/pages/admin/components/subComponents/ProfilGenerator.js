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
            <h2>Générateur de profils</h2>
                <form onSubmit={handleSubmit}>
                    <div className="pGInput">
                        <label htmlFor="prénom">Prénom</label>
                        <input type="text" value={profilName.firstName} name="firstName" onChange={handleChange}/>
                    </div>
                    <div className="pGInput">
                    <label htmlFor="Nom">Nom</label>
                    <input type="text" value={profilName.lastName} name="lastName" onChange={handleChange} />
                    </div>
                    <button>Générer le profil</button>
                </form>
                <div id="loading" style={{display: "none"}}>Loading...</div>
             
        </div>
    )
}