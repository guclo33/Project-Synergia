import React, {useContext, useEffect, useState} from "react";
import { AuthContext } from "../../AuthContext";
import { ProfilGenerator } from "./subComponents/ProfilGenerator";



export function AdminHome() {
    const {user} = useContext(AuthContext)
    
    
    return(
        <div className="AdminHome">
            <ProfilGenerator />
        </div>
    )
}