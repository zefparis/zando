import React, { createContext, useState, useContext } from 'react';
import apiClient from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('zando_token'));

  const login = async (phone_number, pin) => {
    try {
      const response = await apiClient.post('/auth/login', { phone_number, pin });
      const { access_token } = response.data;
      localStorage.setItem('zando_token', access_token);
      setToken(access_token);
      // Idéalement, vous décoderiez le token pour obtenir les infos utilisateur
      // Pour l'instant, on simule un utilisateur connecté.
      setUser({ phone_number }); 
      return true;
    } catch (error) {
      console.error("Erreur de connexion:", error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('zando_token');
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);