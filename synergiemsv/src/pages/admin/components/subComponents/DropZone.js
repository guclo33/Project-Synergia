import React, {useCallback,useContext, useState, useEffect} from "react";
import { useParams } from "react-router";
import { useDropzone } from 'react-dropzone';
import { AuthContext } from "../../../AuthContext";

export function DropZone({detailsData, category, apiUrl}) {
    const [files, setFiles] = useState([]);
    const {user} = useContext(AuthContext)
    const {info} = detailsData
    
    const fetchFiles = useCallback(async () => {
        try {
            const response = await fetch(`${apiUrl}/${category}/list/${info.nom_client}`, {
                method: "GET",
                credentials: "include",
            });
            if (response.ok) {
                const data = await response.json();
                setFiles(data.files);
            }
        } catch (error) {
            console.error("Error fetching files:", error);
        }
    }, [apiUrl, category]);


    const onDrop = useCallback(async (acceptedFiles) => {
        if (!detailsData?.info?.nom_client) {
            console.error("detailsData.info.nom_client is not defined");
            return;
        }
        
        const formData = new FormData();
        formData.append('file', acceptedFiles[0]);

        try {
            const response = await fetch(`${apiUrl}/${category}/upload/${info.nom_client}`, {
                method: "POST",
                credentials : "include",
                body : formData
            });
            if (response.ok) {
                const data = response.json()
                console.log('Uploaded file:', data);
                fetchFiles();
            }
        } catch (error) {
            console.log("couldn't upload file")
        }

    },[user, detailsData]);

    const downloadFile = async (fileName) => {
        try {
            const response = await fetch(`${apiUrl}/${category}/download/${info.nom_client}/${fileName}`, {
                method: "GET",
                credentials: "include",
            });
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                a.remove();
            }
        } catch (error) {
            console.error("Error downloading file:", error);
        }
    };

    useEffect(() => {
        fetchFiles();
    }, [fetchFiles]);

    
    const { getRootProps, getInputProps } = useDropzone({ onDrop });

    return (
        <div>
            <h3>{category}</h3>
            <div {...getRootProps({ className: "dropzone" })} style={{ border: "2px dashed #cccccc", padding: "20px", textAlign: "center" }}>
                <input {...getInputProps()} />
                <p>Drag and drop files here, or click to select files.</p>
            </div>
            <ul>
                {files.map((file, index) => (
                    <li key={index}>
                        {file} <button onClick={() => downloadFile(file)}>Download</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}