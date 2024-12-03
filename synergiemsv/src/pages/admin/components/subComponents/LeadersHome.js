import React, {useState} from "react";
import "../../../pages.css"

export function LeadersHome ({ adminHomeData})  {
    const [active, setActive] = useState(true)

    const handleCheck = () =>{
        
        setActive(!active)
        
        
    }

    const leadersActif = adminHomeData.filter(leader => leader.active !== undefined && leader.active === active);

    return (
        <div className="leadersHome">
            <h3>Vos leaders!</h3>
            <input id = "active" type="checkbox" checked={!active} onChange={handleCheck} />
            <label htmlFor="active">Voir les leaders inactifs</label>

            {leadersActif.map((leader) => (
                <div className="leaderHome" key={leader.id}>   
                    <h4>Leader</h4>
                    <p>{leader.nom}</p>
                    <h4>Courriel</h4>
                    <p>{leader.email}</p>
                    <h4>Téléphone</h4>
                    <p>{leader.phone}</p>
                    <h4>Status</h4>
                    {leader.active ? <p>Actif</p> : <p>Inactif</p>}
                </div>   
            ))}
        </div>
    );
}

