import React, { useState, useEffect, FormEvent } from 'react';
import { apiFetch } from './services/api';

type Role = {
  role_id: string;
  role_name: string;
  role_human_id: number;
};

function getPasswordProblems(password: string, confirmPassword: string) {
  const problems = [
    {
      key: 'no_match',
      label: 'Passwords do not match',
      valid: password === confirmPassword && password.length > 0
    },
    {
      key: 'too_short',
      label: 'Password is too short (min 8 characters)',
      valid: password.length >= 8
    },
    {
      key: 'no_lowercase',
      label: 'At least one lowercase letter',
      valid: /[a-z]/.test(password)
    },
    {
      key: 'no_uppercase',
      label: 'At least one uppercase letter',
      valid: /[A-Z]/.test(password)
    },
    {
      key: 'no_number',
      label: 'At least one number',
      valid: /\d/.test(password)
    },
    {
      key: 'no_special',
      label: 'At least one special character',
      valid: /[^A-Za-z0-9]/.test(password)
    }
  ];
  return problems;
}


function getEmailProblems(email: string) {
  return [
    {
      key: 'invalid_format',
      label: 'Invalid email format',
      valid: /^\S+@\S+\.\S+$/.test(email) && email.length > 0
    }
  ];
}


export default function Register() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState<boolean>(false);
  const [roleId, setRoleId] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    apiFetch('/roles/')
      .then((data: Role[]) => setRoles(data))
      .catch(() => setRoles([]));
  }, []);


  const passwordProblems = getPasswordProblems(password, confirmPassword);
  const emailValid = getEmailProblems(email);
  // Helper to get selectedIndex for the role dropdown
  const getRoleSelectedIndex = () => {
    if (!roleId) return 0;
    const idx = roles.findIndex(r => r.role_id === roleId);
    return idx >= 0 ? idx + 1 : 0;
  };

  const allValid = (
    passwordProblems.every(p => p.valid) &&
    emailValid.every(p => p.valid) &&
  getRoleSelectedIndex() > 0
  );

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    if (!emailValid) {
      setError('Please enter a valid email address.');
      return;
    }
    if (!allValid) {
      setError('Password does not meet all requirements.');
      return;
    }
    if (!roleId) {
      setError('Please select a role.');
      return;
    }
    setLoading(true);
    try {
      await apiFetch('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, confirm_password: confirmPassword, name, role_id: roleId })
      });
      setSuccess('User created successfully!');
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setRoleId('');
    setName('');
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
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <input
            type="text"
            className="mt-1 block w-full border rounded px-3 py-2"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
        </div>
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
          <div className="flex items-center gap-2 mt-1">
            <input
              type={showPassword ? 'text' : 'password'}
              className="block w-full border rounded px-3 py-2"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
            <div>
              <button
                type="button"
                className="text-xs text-gray-600 border border-gray-300 rounded px-2 py-1"
                tabIndex={-1}
                onClick={() => setShowPassword((v) => !v)}
              >
                {showPassword ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Confirm Password</label>
          <div className="flex items-center gap-2 mt-1">
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              className="block w-full border rounded px-3 py-2"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              required
            />
            <div>
              <button
                type="button"
                className="text-xs text-gray-600 border border-gray-300 rounded px-2 py-1"
                tabIndex={-1}
                onClick={() => setShowConfirmPassword((v) => !v)}
              >
                {showConfirmPassword ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>
        </div>
        <div className="mt-2">
          <ul className="space-y-1">
            {passwordProblems.map((p, idx) => (
              <li key={p.key} className="flex items-center gap-2 text-sm">
                <span className={p.valid ? 'text-green-600' : 'text-red-600'}>
                  {p.valid ? '✔' : '✖'}
                </span>
                <span>{p.label}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Role</label>
          <select
            className="mt-1 block w-full border rounded px-3 py-2"
            value={roleId}
            onChange={e => setRoleId(e.target.value)}
            required
          >
            <option value="">Select a role</option>
            {roles.map((r) => (
              <option key={r.role_id} value={r.role_id}>
                {r.role_name} ({r.role_human_id})
              </option>
            ))}
          </select>
        </div>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        {success && <div className="text-green-600 text-sm">{success}</div>}
        <button
          type="submit"
          className={`px-4 py-2 rounded ${allValid && !loading ?
             'bg-blue-600 text-white'
             : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
          disabled={loading || !allValid}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
}
