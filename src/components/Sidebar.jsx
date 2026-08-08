import { NavLink } from 'react-router-dom';
import {
  Grid,
  CloudSun,
  Leaf,
  TrendingUp,
  Lightbulb,
  MapPin,
  User,
  SlidersHorizontal,
} from 'lucide-react';

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: Grid },
  { path: '/weather', label: 'Weather', icon: CloudSun },
  { path: '/crop-health', label: 'Crop Health', icon: Leaf },
  { path: '/prediction', label: 'Prediction', icon: TrendingUp },
  { path: '/recommendation', label: 'Recommendations', icon: Lightbulb },
  { path: '/gis-map', label: 'GIS Map', icon: MapPin },
  { path: '/profile', label: 'Profile', icon: User },
  { path: '/settings', label: 'Settings', icon: SlidersHorizontal },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <p className="sidebar-title">Navigation</p>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}
