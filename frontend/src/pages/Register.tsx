import React, { useState, useEffect, FormEvent } from 'react';
import { apiFetch } from './services/api';

type Role = {
  id: string;
  name: string;
};

function isValidPassword(pwd: string): boolean {
  if (pwd.length < 10) return false;
  let types = 0;
  if (/[a-z]/.test(pwd)) types++;
  if (/[A-Z]/.test(pwd)) types++;
  if (/\d/.test(pwd)) types++;
  if (/[^A-Za-z0-9]/.test(pwd)) types++;
  return types >= 2;
}

export default function Register() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [role, setRole] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    apiFetch('/roles/')
      .then((data: Role[]) => setRoles(data))
      .catch(() => setRoles([]));
  }, []);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (!email.match(/^\S+@\S+\.\S+$/)) {
      setError('Please enter a valid email address.');
      return;
    }
    if (!isValidPassword(password)) {
      setError('Password must be at least 10 characters and contain at least two of: lowercase, uppercase, digit, special character.');
      return;
    }
    if (!role) {
      setError('Please select a role.');
      return;
    }
    setLoading(true);
    try {
      await apiFetch('/users/', {
        method: 'POST',
        body: JSON.stringify({ email, password, role_name: role })
      });
      setSuccess('User created successfully!');
      setEmail('');
      setPassword('');
      setRole('');
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mt-8 mx-auto p-6 bg-white shadow rounded-lg">
      <h2 className="text-lg font-semibold mb-4">Register New User</h2>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            className="mt-1 block w-full border rounded px-3 py-2"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            className="mt-1 block w-full border rounded px-3 py-2"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          <p className="text-xs text-gray-500 mt-1">At least 10 chars, 2+ types: lower, upper, digit, special.</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Role</label>
          <select
            className="mt-1 block w-full border rounded px-3 py-2"
            value={role}
            onChange={e => setRole(e.target.value)}
            required
          >
            <option value="">Select a role</option>
            {roles.map((r) => (
              <option key={r.id} value={r.name}>{r.name}</option>
            ))}
          </select>
        </div>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        {success && <div className="text-green-600 text-sm">{success}</div>}
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
}
