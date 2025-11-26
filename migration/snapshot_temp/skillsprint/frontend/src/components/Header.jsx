import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import ThemeToggle from "./ThemeToggle.jsx";
import { Home as HomeIcon, Trophy, Layers } from "lucide-react";

const Header = () => {
  const { isAuthenticated, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const closeMobile = () => setMobileOpen(false);

  return (
    <header className="glass-card sticky top-0 z-50 border-b border-white/20 dark:border-slate-700/30">
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          <div className="flex-shrink-0">
            <NavLink to="/" className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent hover:from-purple-700 hover:to-blue-700 transition-all duration-300" aria-label="SkillSprint Home">
              Skill<span className="text-indigo-500">Sprint</span> 🚀
            </NavLink>
          </div>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center space-x-2 md:space-x-4">
            <NavLink
              to="/"
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              <span className="inline-flex items-center gap-2"><HomeIcon className="w-4 h-4" aria-hidden="true" /> <span>Home</span></span>
            </NavLink>
            <NavLink
              to="/leaderboard"
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              <span className="inline-flex items-center gap-2"><Trophy className="w-4 h-4" aria-hidden="true" /> <span>Leaderboard</span></span>
            </NavLink>
            <NavLink
              to="/modules"
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              <span className="inline-flex items-center gap-2"><Layers className="w-4 h-4" aria-hidden="true" /> <span>Modules</span></span>
            </NavLink>
            {isAuthenticated && (
              <NavLink
                to="/dashboard"
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              >
                Dashboard
              </NavLink>
            )}

            <ThemeToggle />

            <div className="w-px h-8 bg-gradient-to-b from-transparent via-slate-300 dark:via-slate-600 to-transparent"></div>

            {isAuthenticated ? (
              <button
                onClick={logout}
                className="btn-secondary bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700"
              >
                Logout
              </button>
            ) : (
              <div className="flex items-center space-x-3">
                <NavLink
                  to="/login"
                  className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                >
                  Log In
                </NavLink>
                <NavLink to="/signup" className="btn-primary">
                  Sign Up
                </NavLink>
              </div>
            )}
          </div>

          {/* Mobile controls */}
          <div className="flex items-center md:hidden gap-2">
            <ThemeToggle />
            <button
              aria-label="Toggle menu"
              aria-expanded={mobileOpen}
              onClick={() => setMobileOpen((v) => !v)}
              className="p-2 rounded-lg border border-white/20 dark:border-slate-600/30 bg-white/50 dark:bg-slate-700/50 hover:bg-white/80 dark:hover:bg-slate-700/80 transition"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="w-6 h-6 text-slate-700 dark:text-slate-200"
              >
                {mobileOpen ? (
                  <path
                    fillRule="evenodd"
                    d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 11-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z"
                    clipRule="evenodd"
                  />
                ) : (
                  <path
                    fillRule="evenodd"
                    d="M3.75 6.75A.75.75 0 014.5 6h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75zm0 5.25a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75zm0 5.25a.75.75 0 01.75-.75h15a.75.75 0 010 1.5h-15a.75.75 0 01-.75-.75z"
                    clipRule="evenodd"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu panel */}
        {mobileOpen && (
          <div className="md:hidden py-3 animate-fade-in">
            <div className="flex flex-col gap-2 p-3 glass-card">
              <NavLink
                to="/"
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                onClick={closeMobile}
              >
                <span className="inline-flex items-center gap-2"><HomeIcon className="w-5 h-5" aria-hidden="true" /> <span>Home</span></span>
              </NavLink>
              <NavLink
                to="/leaderboard"
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                onClick={closeMobile}
              >
                <span className="inline-flex items-center gap-2"><Trophy className="w-5 h-5" aria-hidden="true" /> <span>Leaderboard</span></span>
              </NavLink>
              <NavLink
                to="/modules"
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                onClick={closeMobile}
              >
                <span className="inline-flex items-center gap-2"><Layers className="w-5 h-5" aria-hidden="true" /> <span>Modules</span></span>
              </NavLink>
              {isAuthenticated && (
                <NavLink
                  to="/dashboard"
                  className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                  onClick={closeMobile}
                >
                  Dashboard
                </NavLink>
              )}
              <div className="h-px w-full bg-slate-200 dark:bg-slate-700 my-2"></div>
              {isAuthenticated ? (
                <button
                  onClick={() => { logout(); closeMobile(); }}
                  className="btn-secondary bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700"
                >
                  Logout
                </button>
              ) : (
                <div className="grid grid-cols-2 gap-2">
                  <NavLink to="/login" className="btn-secondary text-center" onClick={closeMobile}>
                    Log In
                  </NavLink>
                  <NavLink to="/signup" className="btn-primary text-center" onClick={closeMobile}>
                    Sign Up
                  </NavLink>
                </div>
              )}
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;

