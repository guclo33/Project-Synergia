import React, {useCallback,useContext, useState, useEffect} from "react";
import { useParams } from "react-router";
import { useDropzone } from 'react-dropzone';
import { AuthContext } from "../../../AuthContext";
import { DropZone } from "./DropZone";

export function Document({detailsData}) {
        const {user} = useContext(AuthContext)
        const apiUrl = `http://localhost:3000/api/admin/${user.id}/details/`;
        
        return (
            <div>
                <DropZone detailsData={detailsData} apiUrl={apiUrl} category="profile" />
                <DropZone detailsData={detailsData} apiUrl={apiUrl} category="factures" />
                <DropZone detailsData={detailsData} apiUrl={apiUrl} category="questionnaires" />
            </div>
        );
    }