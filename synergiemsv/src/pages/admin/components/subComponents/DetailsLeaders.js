import React, {useState, useEffect} from "react";
import { useParams } from "react-router";
import { Link } from "react-router-dom";

export function DetailsLeaders({leadersData}) {
   
   
    if(!leadersData) {
        return <h2>...loading</h2>
    }
    
    return(
        <div className="detailsLeader">
            <h3>Liste des leaders:</h3> 
            {leadersData.map(leader => (
                <Link to={`${leader.leader_id}`}><div className="detailsLeaders" key={leader.leader_id}>
                    <h4>{leader.nom}</h4>
                    <p>{leader.email}</p>
                    <p>{leader.phone}</p>

                </div></Link>
            ))}
        </div>
    )
}