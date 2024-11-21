import React from "react";

export function RegisterForm({handleSubmit, handleChange, registerData, passCapsVerified, samePassword, passLength}) {
    return (
        <form onSubmit={handleSubmit}>
            <div className="form">
                <label htmlFor="username">Nom d'utilisateur</label>
                <input type="text" value={registerData.username} id="username" name="username" placeholder="Nom d'utilisateur" onChange={handleChange} />
                <label htmlFor="email">Courriel</label>
                <input type="email" value={registerData.email} id="email" name="email" placeholder="Courriel" onChange={handleChange}/>
                <label htmlFor="password">Mot de passe</label>
                <input type="password" value={registerData.password} id="password" name="password" placeholder="Mot de passe" onChange={handleChange} />
                <label htmlFor="verifyPassword">Vérification du mot de passe</label>
                <input type="password" value={registerData.verifyPassword} id="verifyPassword" name="verifyPassword" placeholder="Mot de passe" onChange={handleChange} />
            </div>
            <div className="verificator">
                <ul>
                    <li style={{ color : passLength ? "green" : "red"}}>Le mot de passe possède de 8 à 32 caractère</li>
                    <li style={{ color : passCapsVerified ? "green" : "red"}}>Le mot de passe possède au moins une majuscule et une minuscule</li>
                    <li style={{ color : samePassword ? "green" : "red"}}>Les deux mots de passe correspondent</li>
                </ul>
            </div>
            <button type="submit" name="submit" placeholder="Soumission">Créer votre compte</button>
        </form>
    )
}