// frontend/src/components/Header.jsx
import { Link, useNavigate } from 'react-router-dom'

export default function Header() {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <header style={{ background: '#eee', padding: '1rem' }}>
      <nav style={{ display: 'flex', gap: '1rem', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <Link to="/">Dashboard</Link>
          {!isLoggedIn && <Link to="/register">Register</Link>}
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          {isLoggedIn ? (
            <button onClick={handleLogout} style={{ cursor: 'pointer' }}>
              Logout
            </button>
          ) : (
            <Link to="/login">Login</Link>
          )}
        </div>
      </nav>
    </header>
  )
}
