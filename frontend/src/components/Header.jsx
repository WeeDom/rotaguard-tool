// frontend/src/components/Header.jsx
import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header style={{ background: '#eee', padding: '1rem' }}>
      <nav style={{ display: 'flex', gap: '1rem' }}>
        <Link to="/">Dashboard</Link>
        <Link to="/login">Login</Link>
        <Link to="/register">Register</Link>
      </nav>
    </header>
  )
}
