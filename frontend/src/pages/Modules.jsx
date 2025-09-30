import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Modules() {
  const { isAuthenticated } = useAuth();

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
        <div className="module-card flex flex-col">
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
        <div className="module-card flex flex-col">
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
