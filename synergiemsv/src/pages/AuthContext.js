import React, { createContext, useState, useEffect } from 'react';
import Cookies from "js-cookie"

export const AuthContext = createContext();

export const  AuthProvider = ({children}) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = Cookies.get('user');
        if (storedUser) {
          setUser(JSON.parse(storedUser)); 
          console.log("User from cookies:", JSON.parse(storedUser))
        }
      }, []);

      const login = (userData) => {
        setUser(userData);
        Cookies.set('user', JSON.stringify(userData), {expires: 7});
      };
    
      
      const logout = () => {
        setUser(null);
        Cookies.remove('user'); 
      };

      return (
        <AuthContext.Provider value={{ user, login, logout }}>
          {children}
        </AuthContext.Provider>
      );
}