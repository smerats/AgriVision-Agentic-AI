import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService.js';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!email || !password) {
      setError('Please enter email and password.');
      return;
    }
    login(email, password);
    navigate('/dashboard');
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <p className="eyebrow">Welcome to AgriTwin AI</p>
          <h1>Smart decisions for smarter farming.</h1>
          <p className="text-muted">Sign in to access your farm digital twin, weather insights, and AI recommendations.</p>
        </div>
        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <p className="error-text">{error}</p>}
          <label>Email</label>
          <input className="input-field" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <label>Password</label>
          <input className="input-field" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button className="primary-button" type="submit">Login</button>
          <button type="button" className="secondary-button" onClick={() => navigate('/register')}>
            Register
          </button>
        </form>
      </div>
    </div>
  );
}
