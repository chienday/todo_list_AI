import { useState, useEffect, createContext, useContext } from 'react';
import authApi from '../api/authApi';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const login = async (credentials) => {
    const response = await authApi.login(credentials);
    authApi.setToken(response.access_token);
    setIsAuthenticated(true);
    return response;
  };

  const logout = () => {
    authApi.removeToken();
    setIsAuthenticated(false);
  };

  useEffect(() => {
    // Check token on mount
    const token = authApi.getToken();
    if (token) {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  // Show loading while checking auth
  if (isLoading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default useAuth;
