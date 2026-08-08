import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { register } from '../services/authService.js';

export default function Register() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [farmLocation, setFarmLocation] = useState('Kochi, Kerala');
  const [cropType, setCropType] = useState('Rice');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!fullName || !email || !password || !confirmPassword) {
      setError('Please complete all fields.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    register({ fullName, email, password, farmLocation, cropType });
    navigate('/dashboard');
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <p className="eyebrow">Create a new account</p>
          <h1>Register for AgriTwin AI</h1>
          <p className="text-muted">Start your farm digital twin journey and unlock precision analytics.</p>
        </div>
        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <p className="error-text">{error}</p>}
          <label>Full name</label>
          <input className="input-field" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          <label>Email</label>
          <input className="input-field" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <label>Password</label>
          <input className="input-field" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <label>Confirm password</label>
          <input className="input-field" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
          <label>Farm location</label>
          <input className="input-field" value={farmLocation} onChange={(e) => setFarmLocation(e.target.value)} />
          <label>Crop type</label>
          <input className="input-field" value={cropType} onChange={(e) => setCropType(e.target.value)} />
          <button className="primary-button" type="submit">Create Account</button>
        </form>
      </div>
    </div>
  );
}
