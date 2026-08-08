import { getCurrentUser, logout } from '../services/authService.js';
import { useNavigate } from 'react-router-dom';

export default function Profile() {
  const user = getCurrentUser();
  const navigate = useNavigate();

  return (
    <div className="profile-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Farmer Profile</p>
          <h1 className="page-title">Account details</h1>
          <p className="page-subtitle">Manage your profile, farm settings, and account information.</p>
        </div>
      </div>

      <div className="card profile-card">
        <div className="profile-grid">
          <div>
            <p className="eyebrow">Name</p>
            <h3>{user?.name}</h3>
          </div>
          <div>
            <p className="eyebrow">Email</p>
            <h3>{user?.email}</h3>
          </div>
          <div>
            <p className="eyebrow">Farm location</p>
            <h3>{user?.location}</h3>
          </div>
          <div>
            <p className="eyebrow">Farm size</p>
            <h3>{user?.farmSize}</h3>
          </div>
          <div>
            <p className="eyebrow">Main crop</p>
            <h3>{user?.mainCrop}</h3>
          </div>
        </div>
        <button className="small-button secondary-button" onClick={() => navigate('/settings')}>
          Edit Profile
        </button>
      </div>
      <div className="card profile-action-card">
        <h4>Security</h4>
        <p>Use the settings panel to manage notification alerts, account privacy, and units.</p>
        <button className="small-button primary-button" onClick={() => { logout(); navigate('/login'); }}>
          Logout
        </button>
      </div>
    </div>
  );
}
