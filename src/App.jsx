import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { isAuthenticated } from './services/authService.js';
import Navbar from './components/Navbar.jsx';
import Sidebar from './components/Sidebar.jsx';
import Footer from './components/Footer.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Weather from './pages/Weather.jsx';
import CropHealth from './pages/CropHealth.jsx';
import Prediction from './pages/Prediction.jsx';
import Recommendation from './pages/Recommendation.jsx';
import GISMap from './pages/GISMap.jsx';
import Profile from './pages/Profile.jsx';
import Settings from './pages/Settings.jsx';

function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function AppLayout({ children }) {
  return (
    <div className="app-shell">
      <Navbar />
      <div className="app-body">
        <Sidebar />
        <main className="app-content">{children}</main>
      </div>
      <Footer />
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <AppLayout>
                <Routes>
                  <Route path="dashboard" element={<Dashboard />} />
                  <Route path="weather" element={<Weather />} />
                  <Route path="crop-health" element={<CropHealth />} />
                  <Route path="prediction" element={<Prediction />} />
                  <Route path="recommendation" element={<Recommendation />} />
                  <Route path="gis-map" element={<GISMap />} />
                  <Route path="profile" element={<Profile />} />
                  <Route path="settings" element={<Settings />} />
                  <Route path="" element={<Navigate to="/dashboard" replace />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </AppLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
