import React, {useEffect, useState, useContext} from "react";
import { AuthContext } from "../../AuthContext";

export function Overview() {
    const [overviewData, setOverviewData] = useState([])
    const [modifyId, setModifyId] = useState(null);
    const [newInfos, setNewInfos] = useState({
        date_presentation : overviewData.date_presentation,
        echeance : overviewData.echeance,
        statut: overviewData.statut,
        priorite : overviewData.priorite
    })

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
        
    }, [user, overviewData])
    
    const handleClick = (e) =>{
        const leaderID = e.target.getAttribute("data-id")
        setModifyId(leaderID)
    }

    const handleChange = (e) => {
        const {name, value} = e.target;
        setNewInfos(prev => ({
            ...prev,
            [name] : value
        }))

    }

    const handleCancelButton = () =>{
        setModifyId(null)
    }

    const handleSubmit = async (e) =>  {
        e.preventDefault()
        console.log(`leaderid: ${modifyId}, date presentation: ${newInfos.date_presentation}, echeance: ${newInfos.echeance}, statut: ${newInfos.statut}, priorite: ${newInfos.priorite}`)
        try{
            const response = await fetch(`http://localhost:3000/api/admin/${user.id}/overview`, {
                method : "PUT",
                credentials : "include",
                headers : {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({
                    leader_id : modifyId,
                    date_presentation: newInfos.date_presentation,
                    echeance: newInfos.echeance,
                    statut: newInfos.statut,
                    priorite: newInfos.priorite
                })
            });
            if(response.ok){
                console.log(`overview for leaderId ${modifyId}data are succesfully updated`)
                setModifyId(null)
            } else {
                console.log("error while trying to update in the server")
            }
        } catch(error) {
            console.log("couldn't update leader overview data" , error)
        }
    }
    
    return(
        <div className="Overview">
            <h2>Tableau de bord: vue d'ensemble</h2>
            
            {overviewData.map(leader => (
                modifyId == leader.leader_id ? (
                    <form onSubmit={handleSubmit} className="modifyForm">
                        <h4>{leader.nom}</h4>     

                        <h5>Date de présentation :</h5>
                        <input type="datetime-local" name="date_presentation" value={newInfos.date_presentation || leader.date_presentation || ""} onChange={handleChange} />

                        <h5>Date d'échéance :</h5>
                        <input type="date" name="echeance" value={newInfos.echeance || leader.echeance || ""}  onChange={handleChange} />

                        <h5>Statut :</h5>
                        <select name="statut" value={newInfos.statut || leader.statut || ""} onChange={handleChange}> 
                            <option value="À faire">À faire</option>
                            <option value="En cours">En cours</option>
                            <option value="Terminé">Terminé</option>
                        </select>

                        <h5>Priorité :</h5>
                        <select name="priorite" value={newInfos.priorite || leader.priorite || ""} onChange={handleChange}>
                            <option value="Faible">Faible</option>
                            <option value="Moyenne">Moyenne</option>
                            <option value="Élevé">Élevé</option>
                        </select>
                        <button onClick={handleCancelButton}>Annuler</button>
                        <button type="submit" name="modify">Confirmé</button>
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

                    <button data-id={leader.leader_id} name="modify" onClick={handleClick}>Modifier</button>
                </div>)
            ))}
        </div>
    )
}