import React, {useEffect, useState, useContext} from "react";
import { AuthContext } from "../../AuthContext";

export function Overview() {
    const [overviewData, setOverviewData] = useState([])
    const [modifyId, setModifyId] = useState(false)

    const {user} = useContext(AuthContext)

    useEffect(() => {
        const getOverviewData = async () => {
            try {
                const response = await fetch(`http://localhost:3000/api/admin/${user.id}/overview`, {
                    method: "GET",
                    credentials: "include",
                    });
                    if(response.ok){
                        const data = await response.json();
                        console.log("here's data", data.rows)
                        const dataArray = data.rows.map((row) => ( {
                            leader_id: row.leader_id,
                            nom: row.nom,
                            date_presentation: row.date_presentation,
                            echeance: row.echeance,
                            statut: row.statut,
                            priorite: row.priorite
                        }));
                        console.log("dataArray:", dataArray)
                        setOverviewData(dataArray)
                        console.log("overviewData:", overviewData)
                        
                        
                    } else {
                        const errorText = await response.text();
                        console.error("Error response from server:", errorText)
                };
            } catch(error) {
                console.error("Could not connect to getadminhomedata", error)
            }
        }

        

        getOverviewData();
        
    }, [user])
    
    const handleClick = () =>{
        setModify(!modify)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
    }
    
    return(
        <div className="Overview">
            <h2>Tableau de bord: vue d'ensemble</h2>
            
            {overviewData.map(leader => (
                modifyId === leader.leader_id ? (
                    <form onSubmit={handleSubmit}>
                        <h4>{leader.nom}</h4>                       
                        <h5>Date de présentation :</h5>
                        <p>{leader.date_presentation}</p>
                        <h5>Date d'échéance :</h5>
                        <p>{leader.echeance}</p>
                        <h5>Statut :</h5>
                        <p>{leader.statut}</p>
                        <h5>Priorité :</h5>
                        <p>{leader.priorite}</p>
                        <button type="submit" name="modify">Modifier</button>
                    </form>
                ) : (
                <div className="overviewLeader" key={leader.leader_id}>
                    
                    <h4>{leader.nom}</h4>
                    <h5>Date de présentation :</h5>
                    <p>{leader.date_presentation}</p>
                    <h5>Date d'échéance :</h5>
                    <p>{leader.echeance}</p>
                    <h5>Statut :</h5>
                    <p>{leader.statut}</p>
                    <h5>Priorité :</h5>
                    <p>{leader.priorite}</p>

                    <button name="modify" onClick={handleClick}>Modifier</button>
                </div>)
            ))}
        </div>
    )
}