import React, { useState, useEffect } from "react";
import api from "../services/api"; // Correctly import the api service

const Leaderboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true);
        // MODIFIED: Use the correct named function from the api service
        const response = await api.getLeaderboard();
        setUsers(response.data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch leaderboard data. Please try again later.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-12">
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-slate-800 dark:text-slate-100 leading-tight">
          Top Performers
        </h1>
        <p className="text-lg text-gray-600 mt-2">
          See who is leading the charge in our daily challenges!
        </p>
      </div>

      {loading && <p className="text-center text-gray-500">Loading leaderboard...</p>}
      {error && <p className="text-center text-red-500 bg-red-100 p-4 rounded-lg">{error}</p>}
      
      {!loading && !error && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg overflow-hidden">
          <table className="min-w-full leading-normal">
            <thead>
              <tr>
                <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-slate-700 bg-gray-100 dark:bg-slate-800 text-left text-xs font-semibold text-gray-600 dark:text-slate-300 uppercase tracking-wider">
                  Rank
                </th>
                <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-slate-700 bg-gray-100 dark:bg-slate-800 text-left text-xs font-semibold text-gray-600 dark:text-slate-300 uppercase tracking-wider">
                  User
                </th>
                <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-slate-700 bg-gray-100 dark:bg-slate-800 text-left text-xs font-semibold text-gray-600 dark:text-slate-300 uppercase tracking-wider">
                  XP
                </th>
                <th className="px-5 py-3 border-b-2 border-gray-200 dark:border-slate-700 bg-gray-100 dark:bg-slate-800 text-left text-xs font-semibold text-gray-600 dark:text-slate-300 uppercase tracking-wider">
                  Streak
                </th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, index) => (
                <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-slate-700">
                  <td className="px-5 py-5 border-b border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm">
                    <p className="text-gray-900 dark:text-white whitespace-no-wrap font-bold">{index + 1}</p>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm">
                    <p className="text-gray-900 dark:text-white whitespace-no-wrap">{user.username}</p>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm">
                    <p className="text-gray-900 dark:text-white whitespace-no-wrap">{user.xp}</p>
                  </td>
                  <td className="px-5 py-5 border-b border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm">
                     <p className="text-gray-900 dark:text-white whitespace-no-wrap">{user.streak} 🔥</p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;

