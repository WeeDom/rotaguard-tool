import React, { useState, useEffect } from 'react';
import { getCurrentUser } from './services/api.js';

interface User {
  id: string;
  email: string;
  name: string;
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchUser() {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
        // If there's an error (like token expired), redirect to login
        if (error instanceof Error && error.message.includes('401')) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, []);

  // Extract first name from full name
  const getFirstName = (fullName: string): string => {
    return fullName.split(' ')[0];
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-300 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-300 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-600">
          {user ? `Welcome back, ${getFirstName(user.name)}` : 'Welcome back'}. Here's what's happening with your rota.
        </p>
      </header>
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-sm font-medium text-gray-500">Total Employees</h2>
          <p className="text-2xl font-semibold text-gray-800">42</p>
        </div>
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-sm font-medium text-gray-500">Shifts This Week</h2>
          <p className="text-2xl font-semibold text-gray-800">128</p>
        </div>
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="text-sm font-medium text-gray-500">Compliance Flags</h2>
          <p className="text-2xl font-semibold text-red-600">3</p>
        </div>
      </section>
    </div>
  );
}
