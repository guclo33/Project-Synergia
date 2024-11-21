import React from "react";

export function LoginForm({handleSubmit}) {
    return (
        <form handleSubmit={handleSubmit}>
            <label htmlFor="username">Nom d'utilisateur ou courriel</label>
            <input type="text" value="" id="username" name="username" placeholder="Nom d'utilisateur ou courriel" />
           
            <label htmlFor="password">Mot de passe</label>
            <input type="password" value="" id="password" name="password" placeholder="Mot de passe" />
            
            <button type="submit" name="submit" placeholder="Soumission">Créer votre compte</button>
        </form>
    )
}