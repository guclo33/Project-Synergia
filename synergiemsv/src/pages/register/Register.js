import React from "react";
import image from "../../Images/logo2 sans fond.png"
import {RegisterForm} from "./components/RegisterForm"
import { useNavigate } from "react-router";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

export function Register() {
    const [passCapsVerified, setPassCapsVerified] = useState(false);
    const [samePassword, setSamePassword] = useState(false);
    const [passLength, setPassLength] = useState(false);
    const [verified, setVerified] = useState(false)
    const [registerData, setRegisterData] = useState({
        username : "",
        email: "",
        password: "",
        verifyPassword: ""
    })

    const navigate = useNavigate()

    const isPassCapsVerified = (password) => {
        const minorExist = /[a-z]/.test(password);
        const majorExist = /[A-Z]/.test(password);
        if(minorExist & majorExist) {
            setPassCapsVerified(true)
        } else {
            setPassCapsVerified(false)
        }
    }


    const isPassLength = (password) => {
        if(password.length >= 8 && password.length <=32) {
            setPassLength(true)
        } else {
            setPassLength(false)
        }
    }

    const isSamePassword = (password, verifyPassword) => {
        if(password === verifyPassword){
            setSamePassword(true)
        } else {
            setSamePassword(false)
        }
    }

    useEffect(() => {
        isPassCapsVerified(registerData.password);
        isPassLength(registerData.password);
        isSamePassword(registerData.password, registerData.verifyPassword)
        if(passCapsVerified & passLength & samePassword) {
            setVerified(true)
        } else {
            setVerified(false)
        }

    }, [registerData])


    const handleChange = (e) => {
        const {name, value} = e.target;
        setRegisterData((prev) => ({
            ...prev,
            [name]: value
        }))
    };



    const handleSubmit = async (e) => {
        e.preventDefault();
        if(verified){

        try {
            const response = await fetch ("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(registerData)
            });
            if(response.ok) {
                const data = await response.json()
                console.log("user created!", data)
                navigate("/login")
            } else {
                const errorData = await response.json()
                console.log("Error", errorData.message)
            }

        } catch(error) {
            console.log("Could not create user")
        }
    } else {
        console.log("format de mot de passe non valide")
    }
    };


    return(
        <>
            <nav>
                <ul>
                    <li><a href="https://www.synergiemsv.com">Synergie MSV</a></li>
                    <li><Link to="/">Accueil</Link></li>
                    <li><Link to="/login">Se connecter</Link></li>
                    <li><Link to="/register">Créer un compte</Link></li>
                </ul>
            </nav>
            <div className="register">
                <img src={image} alt="logo SynergieMSV" />
                <RegisterForm handleSubmit={handleSubmit} handleChange={handleChange} registerData={registerData} passCapsVerified={passCapsVerified} samePassword={samePassword} passLength={passLength}/>
            </div>
        </>
    )
}