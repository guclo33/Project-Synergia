import React, {useState,  useContext} from "react";
import { useParams } from "react-router";
import { AuthContext } from "../../../AuthContext";

export function GeneralInfos({detailsData}) {
    const {info, equipe} = detailsData
    const [modify, setModify] = useState(false)
    const [newInfos, setNewInfos] = useState({
        email : info.email,
        phone: info.phone,
        price_sold: info.price_sold,
        active: info.active,
        additional_infos: info.additional_infos
    })
    const {clientid} = useParams()
    const {user} = useContext(AuthContext)
    
    const handleModify = () => {
        setModify(true)
    }
    
    const handleChange = (e) => {
        const {name, value} = e.target;
        setNewInfos((prev) => ({
            ...prev,
            [name] : value
        }))
    }
    const handleCancel = () => {
        setModify(false)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        try{
            const response = await fetch(`http://localhost:3000/api/admin/${user.id}/details/${clientid}`, {
                method : "PUT",
                credentials : "include",
                headers : {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({
                    email : newInfos.email,
                    phone: newInfos.phone,
                    price_sold: newInfos.price_sold,
                    active: newInfos.active,
                    additional_infos: newInfos.additional_infos
                })
            });
            if(response.ok){
                console.log(`overview for client ${clientid}data are succesfully updated`)
                setModify(null)
            } else {
                console.log("error while trying to update in the server")
            }
        } catch(error) {
            console.log("couldn't update client details data" , error)
        }
    }
    
    return(
        <div className="generalInfos">
           <h3>{info.nom_client}</h3>
           {modify ? (
                <form onSubmit={handleSubmit} className="modify">
                    <h5>Courriel :</h5>
                    <input type="email" name="email" value={newInfos.email || ""} onChange={handleChange} />
                    <h5>Téléphone :</h5>
                    <input type="phone" name="phone" value={newInfos.phone || ""} onChange={handleChange} />
                    <h5>Montant de la vente :</h5>
                    <input type="float" name="price_sold" value={newInfos.price_sold || ""} onChange={handleChange} />
                    <h5>Date Échéance :</h5>
                    <input type="date" name="echeance" value={newInfos.echeance || ""} onChange={handleChange} />
                    <h5>Actif ?</h5>
                    <select name="active" value={newInfos.active || ""} onChange={handleChange}>
                            <option value={true}>Oui</option>
                            <option value={false}>Non</option>
                        </select>
                    <h5>Informations supplémentaires :</h5>
                    <input type="text" name="additional_infos" value={newInfos.additional_infos || ""} onChange={handleChange} />
                    <button onClick={handleCancel}>Annuler</button>
                    <button type="submit">Confirmer</button>
                </form>
           ): (
            <div className="modifiableInfos">
                <h5>Courriel :</h5>
                <p>{info.email}</p>
                <h5>Téléphone :</h5>
                <p>{info.phone}</p>
                <h5>Montant de la vente :</h5>
                <p>{info.price_sold}</p>
                <h5>Date Échéance :</h5>
                <p>{info.echeance}</p>
                <h5>Actif ?</h5>
                <p>{info.active ? "Oui" : "Non"}</p>
                <h5>Informations supplémentaires :</h5>
                <p>{info.additional_infos}</p>
                <button name="modify" onClick={handleModify}>Modifier</button>
            </div>
        )}
            <div className="team">
                <h4>Équipe:</h4>
                {equipe.map(user => (
                    <div className="user" key={user.id}>
                        <h4>{user.nom}</h4>
                        <p>Courriel:</p>
                        <p>{user.email}</p>
                        <p>Téléphone:</p>
                        <p>{user.phone}</p>
                    </div>
                ))}
            </div>
        </div>

    )
}