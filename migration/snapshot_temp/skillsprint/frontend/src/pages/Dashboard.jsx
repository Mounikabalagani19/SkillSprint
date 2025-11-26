import React, { useState, useEffect, useRef } from "react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext.jsx";

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isAuthenticated } = useAuth();
  
  // For streak animation
  const streakRef = useRef(null);
  const previousStreak = useRef(null);

  useEffect(() => {
    const fetchUserData = async () => {
      if (isAuthenticated) {
        try {
          setLoading(true);
          const response = await api.getMe();
          setUser(response.data);
          // Store the initial streak value
          if (previousStreak.current === null) {
            previousStreak.current = response.data.streak;
          }
          setError(null);
        } catch (err) {
          setError("Failed to fetch user data. Please try logging in again.");
          console.error(err);
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };
    fetchUserData();
  }, [isAuthenticated]);

  // Effect to handle streak animation
  useEffect(() => {
    if (user && streakRef.current && previousStreak.current !== null) {
      const currentStreak = user.streak;
      const prevStreak = previousStreak.current;
      const element = streakRef.current;

      if (currentStreak > prevStreak) {
        element.classList.add('streak-up');
      } else if (currentStreak < prevStreak) {
        element.classList.add('streak-down');
      }

      const timer = setTimeout(() => {
        element.classList.remove('streak-up', 'streak-down');
      }, 600); // Duration of the animation

      // Update the previous streak for the next comparison
      previousStreak.current = currentStreak;
      
      return () => clearTimeout(timer);
    }
  }, [user]);

  if (loading) return <p className="text-center text-gray-500 dark:text-gray-400">Loading your dashboard...</p>;
  if (!isAuthenticated) return <p className="text-center text-red-500">Please log in to view your dashboard.</p>;
  if (error) return <p className="text-center text-red-500 bg-red-100 dark:bg-red-900/50 p-4 rounded-lg">{error}</p>;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-left mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-800 dark:text-gray-100">
          Welcome, {user ? user.username : 'SprintRunner'}!
        </h1>
        <p className="text-lg text-gray-500 dark:text-gray-400 mt-2">
          Here's a look at your progress. Keep up the great work!
        </p>
      </div>

      {user && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Glassmorphism Cards */}
          <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-lg rounded-2xl shadow-lg border border-white/20 p-6 text-center transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
            <div className="text-5xl font-bold text-indigo-500 dark:text-indigo-400">{user.xp}</div>
            <div className="text-lg font-semibold text-gray-700 dark:text-gray-300 mt-2">Experience Points (XP)</div>
          </div>
          <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-lg rounded-2xl shadow-lg border border-white/20 p-6 text-center transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
            <div ref={streakRef} className="text-5xl font-bold text-orange-500">{user.streak} 🔥</div>
            <div className="text-lg font-semibold text-gray-700 dark:text-gray-300 mt-2">Daily Streak</div>
          </div>
          <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-lg rounded-2xl shadow-lg border border-white/20 p-6 text-center transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
            <div className="text-xl font-bold text-gray-800 dark:text-gray-200 break-all">{user.email}</div>
            <div className="text-lg font-semibold text-gray-700 dark:text-gray-300 mt-2">Account Email</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

