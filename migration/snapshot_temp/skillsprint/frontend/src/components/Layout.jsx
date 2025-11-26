// src/components/Layout.jsx

import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';

function Layout() {
  return (
    // Use a light gray background for the whole page for better contrast
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main>
        {/* This is the key change. This div wraps all your page content.
          - `max-w-7xl`: Sets a maximum width for the content area on large screens.
          - `mx-auto`: This is the magic that centers the container horizontally.
          - `py-6 sm:px-6 lg:px-8`: Adds vertical and horizontal padding that adjusts for screen size.
        */}
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Outlet /> {/* This is where your individual pages (Home, Dashboard, etc.) will be rendered */}
        </div>
      </main>
    </div>
  );
}

export default Layout;

