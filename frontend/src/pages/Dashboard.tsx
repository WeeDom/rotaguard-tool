import React from 'react';

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-600">Welcome back. Here's what's happening with your rota.</p>
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
