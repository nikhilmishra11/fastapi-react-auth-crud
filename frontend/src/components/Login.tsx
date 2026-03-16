import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { loginSuccess } from '../store/authSlice';

const Login: React.FC = () => {
  const [searchParams] = useSearchParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    // If the auth callback redirects here, logic should capture token.
    // However, we handle the callback centrally in App.tsx or here directly.
    const token = searchParams.get('token');
    if (token) {
      dispatch(loginSuccess(token));
      navigate('/dashboard');
    }
  }, [searchParams, dispatch, navigate]);

  const handleOIDCLogin = () => {
    // Redirect to Auth Microservice
    const AUTH_URL = (import.meta as any).env?.VITE_AUTH_URL || 'http://localhost:8001';
    window.location.href = `${AUTH_URL}/auth/login`;
  };

  return (
    <div className="login-container">
      <div className="glass-panel">
        <h1>Welcome Back</h1>
        <p>Access your items securely</p>
        <button onClick={handleOIDCLogin} className="btn primary-btn">
          Login with SSO
        </button>
      </div>
    </div>
  );
};

export default Login;
