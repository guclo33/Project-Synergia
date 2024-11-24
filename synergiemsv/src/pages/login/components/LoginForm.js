import React from "react";

export function LoginForm({handleSubmit, handleChange, userData}) {
    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="usernameOrEmail">Nom d'utilisateur ou courriel</label>
            <input type="text" value={userData.usernameOrEmail} id="username" name="usernameOrEmail" placeholder="Nom d'utilisateur ou courriel" onChange={handleChange} />
           
            <label htmlFor="password">Mot de passe</label>
            <input type="password" value={userData.password} id="password" name="password" placeholder="Mot de passe" onChange={handleChange} />
            
            <button type="submit" name="submit" placeholder="Soumission">Se connecter</button>
        </form>
    )
}