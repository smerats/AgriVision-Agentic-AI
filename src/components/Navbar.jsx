import { Bell, Menu, Search, MapPin, UserCircle2 } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const [searchValue, setSearchValue] = useState('');

  return (
    <header className="navbar shell-card">
      <div className="navbar-left">
        <div className="brand-block">
          <div className="brand-icon">🌾</div>
          <div>
            <p className="brand-name">AgriTwin AI</p>
            <p className="brand-subtitle">Hyper-local farm intelligence</p>
          </div>
        </div>
      </div>
      <div className="navbar-center">
        <div className="search-box">
          <Search size={16} />
          <input
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            placeholder="Search insights, fields, alerts..."
          />
        </div>
      </div>
      <div className="navbar-right">
        <button className="icon-button">
          <Bell size={20} />
        </button>
        <div className="profile-summary">
          <UserCircle2 size={32} />
          <div>
            <p className="profile-name">Farmer Asha</p>
            <p className="profile-location">
              <MapPin size={14} /> Kochi, India
            </p>
          </div>
        </div>
        <button className="icon-button mobile-menu">
          <Menu size={20} />
        </button>
      </div>
    </header>
  );
}
