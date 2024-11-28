import React, { createContext, useState, useEffect } from 'react';
import Cookies from "js-cookie"

export const AuthContext = createContext();

export const  AuthProvider = ({children}) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
      const storedUser = Cookies.get('user');
      
      if (storedUser) {
        try {
          const parsedUser = JSON.parse(storedUser);
          setUser(parsedUser);
          console.log("User from cookies:", parsedUser);
          
        } catch (error) {
          console.error("Error parsing user from cookies:", error);
        }}
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