import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [joinCode, setJoinCode] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await api.createUser({
        username,
        email,
        password,
        role,
        join_code: joinCode || null
      });
      navigate("/login");
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || "Failed to create an account.");
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
      console.error(err);
    }
  };

  return (
    <div className="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      {/* MODIFIED: Applied glassmorphism and dark mode styles */}
      <div className="max-w-md w-full space-y-8 bg-white/50 dark:bg-gray-800/50 backdrop-blur-lg p-10 rounded-2xl shadow-lg border border-white/20">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-gray-100">
            Create your account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300 px-4 py-3 rounded-md" role="alert">
              <span>{error}</span>
            </div>
          )}
          <div className="space-y-4">
            <div className="flex flex-col space-y-2">
              <label className="text-sm font-medium text-slate-500 uppercase tracking-wider">I am a...</label>
              <div className="grid grid-cols-2 gap-2">
                {['student', 'mentor', 'admin', 'guest'].map((r) => (
                  <button
                    key={r}
                    type="button"
                    onClick={() => setRole(r)}
                    className={`py-2 px-4 rounded-xl border-2 transition-all duration-200 capitalize ${role === r
                        ? 'border-purple-600 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 font-bold'
                        : 'border-slate-200 dark:border-slate-700 bg-transparent text-slate-600 dark:text-slate-400'
                      }`}
                  >
                    {r}
                  </button>
                ))}
              </div>
            </div>

            <div className="rounded-xl shadow-sm overflow-hidden border border-slate-200 dark:border-slate-700">
              <div>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  className="w-full px-4 py-3 border-b border-slate-200 dark:border-slate-700 bg-white/50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800 dark:text-gray-200"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="w-full px-4 py-3 border-b border-slate-200 dark:border-slate-700 bg-white/50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800 dark:text-gray-200"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  required
                  className={`w-full px-4 py-3 bg-white/50 dark:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800 dark:text-gray-200 ${(role === 'mentor' || role === 'student') ? 'border-b border-slate-200 dark:border-slate-700' : ''
                    }`}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              {(role === 'mentor' || role === 'student') && (
                <div>
                  <input
                    id="joinCode"
                    name="joinCode"
                    type="text"
                    required
                    className="w-full px-4 py-3 bg-purple-50/50 dark:bg-purple-900/10 focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800 dark:text-gray-200"
                    placeholder={role === 'mentor' ? "Admin Join Code" : "Mentor Join Code"}
                    value={joinCode}
                    onChange={(e) => setJoinCode(e.target.value)}
                  />
                </div>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
            >
              Create Account
            </button>
          </div>
        </form>
        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;

