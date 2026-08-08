import { useState } from 'react';

export default function Settings() {
  const [notifications, setNotifications] = useState(true);
  const [weatherAlerts, setWeatherAlerts] = useState(true);
  const [language, setLanguage] = useState('English');
  const [units, setUnits] = useState('Metric');
  const [theme, setTheme] = useState('Light');

  return (
    <div className="settings-page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Settings</p>
          <h1 className="page-title">Notification and account preferences</h1>
          <p className="page-subtitle">Adjust weather alerts, units, theme, and farm notifications.</p>
        </div>
      </div>

      <div className="grid-2">
        <div className="card settings-card">
          <h4>Alert settings</h4>
          <div className="setting-row">
            <span>Notifications</span>
            <label className="toggle-switch">
              <input type="checkbox" checked={notifications} onChange={() => setNotifications((prev) => !prev)} />
              <span />
            </label>
          </div>
          <div className="setting-row">
            <span>Weather alerts</span>
            <label className="toggle-switch">
              <input type="checkbox" checked={weatherAlerts} onChange={() => setWeatherAlerts((prev) => !prev)} />
              <span />
            </label>
          </div>
        </div>

        <div className="card settings-card">
          <h4>Preferences</h4>
          <label>Language</label>
          <select className="select-field" value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option>English</option>
            <option>Malayalam</option>
            <option>Hindi</option>
          </select>
          <label>Units</label>
          <select className="select-field" value={units} onChange={(e) => setUnits(e.target.value)}>
            <option>Metric</option>
            <option>Imperial</option>
          </select>
          <label>Theme</label>
          <select className="select-field" value={theme} onChange={(e) => setTheme(e.target.value)}>
            <option>Light</option>
            <option>Dark</option>
          </select>
        </div>
      </div>

      <div className="card account-card">
        <h4>Account</h4>
        <p className="text-muted">Manage your login, data sync settings, and connected services later.</p>
        <div className="setting-row">
          <span>Connected backend</span>
          <strong>Demo mode</strong>
        </div>
      </div>
    </div>
  );
}
