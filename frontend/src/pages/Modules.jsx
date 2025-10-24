import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Modules() {
  const { isAuthenticated } = useAuth();
  const [favourites, setFavourites] = useState([]);

  useEffect(() => {
    try {
      const raw = localStorage.getItem("favouriteModules");
      setFavourites(raw ? JSON.parse(raw) : []);
    } catch (e) {
      setFavourites([]);
    }
  }, []);

  const toggleFavourite = (slug) => {
    setFavourites((prev) => {
      const next = prev.includes(slug) ? prev.filter((s) => s !== slug) : [...prev, slug];
      try {
        localStorage.setItem("favouriteModules", JSON.stringify(next));
      } catch (e) {
        // ignore localStorage errors
      }
      return next;
    });
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-slate-800 dark:text-slate-100">Modules</h1>
        <p className="text-slate-600 dark:text-slate-300 mt-3 max-w-2xl mx-auto">
          Choose a module to practice anytime. Earn 5 XP and +1 streak per correct answer. Wrong answers use the same rules as the daily quiz.
        </p>
      </div>

      {!isAuthenticated && (
        <div className="glass-card p-4 text-center max-w-2xl mx-auto mb-8">
          <p className="text-slate-700 dark:text-slate-200">
            Please log in to access module quizzes.
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        <div className="module-card flex flex-col relative">
          <button
            aria-label="Toggle favourite Python"
            onClick={() => toggleFavourite('python')}
            className={`absolute right-4 top-4 w-9 h-9 inline-flex items-center justify-center rounded-full transition-shadow shadow-sm border ${favourites.includes('python') ? 'text-rose-500 bg-rose-50/30 border-rose-100/30' : 'text-slate-300 bg-slate-800/40 border-white/5 hover:text-rose-500 hover:bg-rose-50/8'}`}
            title={favourites.includes('python') ? 'Unfavourite' : 'Favourite'}
          >
            {/* Symmetric heart icon (Heroicons-style) with a 1px upward nudge for visual centering */}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4" style={{ transform: 'translateY(-1px)' }}>
              <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L12 8.343l3.172-3.171a4 4 0 115.656 5.656L12 21.657 3.172 10.828a4 4 0 010-5.656z" clipRule="evenodd" />
            </svg>
          </button>
          <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">Python</h2>
          <p className="text-slate-600 dark:text-slate-300 mt-2 flex-grow">Programming Skills Quiz: Beginner, Intermediate, and Expert difficulties.</p>
          <Link
            to={`/modules/python`}
            className={`btn-primary mt-6 ${!isAuthenticated ? 'pointer-events-none opacity-60' : ''}`}
            aria-disabled={!isAuthenticated}
          >
            Choose Difficulty
          </Link>
        </div>
        <div className="module-card flex flex-col relative">
          <button
            aria-label="Toggle favourite Java"
            onClick={() => toggleFavourite('java')}
            className={`absolute right-4 top-4 w-9 h-9 inline-flex items-center justify-center rounded-full transition-shadow shadow-sm border ${favourites.includes('java') ? 'text-rose-500 bg-rose-50/30 border-rose-100/30' : 'text-slate-300 bg-slate-800/40 border-white/5 hover:text-rose-500 hover:bg-rose-50/8'}`}
            title={favourites.includes('java') ? 'Unfavourite' : 'Favourite'}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4" style={{ transform: 'translateY(-1px)' }}>
              <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L12 8.343l3.172-3.171a4 4 0 115.656 5.656L12 21.657 3.172 10.828a4 4 0 010-5.656z" clipRule="evenodd" />
            </svg>
          </button>
          <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">Java</h2>
          <p className="text-slate-600 dark:text-slate-300 mt-2 flex-grow">Programming Skills Quiz: Beginner, Intermediate, and Expert difficulties.</p>
          <Link
            to={`/modules/java`}
            className={`btn-primary mt-6 ${!isAuthenticated ? 'pointer-events-none opacity-60' : ''}`}
            aria-disabled={!isAuthenticated}
          >
            Choose Difficulty
          </Link>
        </div>
      </div>
    </div>
  );
}
