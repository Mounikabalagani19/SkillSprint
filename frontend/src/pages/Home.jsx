import React, { useState, useEffect } from "react";
import api from "../services/api";
import ChallengeCard from "../components/ChallengeCard.jsx";

const Home = () => {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        setLoading(true);
        const response = await api.getChallenges();
        setChallenges(response.data);
        setError(null);
      } catch (err) {
        setError("Failed to fetch challenges. The server might be down.");
        console.error("Fetch challenges error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchChallenges();
  }, []);

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-16">
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-slate-800 dark:text-slate-100 leading-tight">
          Daily Challenges to
          <span className="block bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent animate-pulse">
            Sharpen Your Mind
          </span>
        </h1>
        <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mt-6 max-w-3xl mx-auto leading-relaxed">
          Join SkillSprint and turn a few minutes a day into a fun, rewarding learning habit.
        </p>
      </div>

      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-700 dark:text-slate-200 mb-8 text-left">
          {(() => {
            // Try to extract a day number from challenges (either a 'day' field or from title "Day N")
            let dayLabel = null;
            if (challenges && challenges.length > 0) {
              const first = challenges[0];
              if (first.day) {
                dayLabel = ` (Day ${first.day})`;
              } else if (first.title) {
                const m = first.title.match(/Day\s*(\d+)/i);
                if (m) dayLabel = ` (Day ${m[1]})`;
              }
            }
            return `Today's Challenges${dayLabel || ''}`;
          })()}
        </h2>
        
        {loading && (
          <div className="text-center py-16">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
            <p className="text-slate-500 dark:text-slate-400 mt-4 text-lg">Loading challenges...</p>
          </div>
        )}
        
        {error && (
          <div className="text-center py-8">
            <div className="glass-card p-6 max-w-md mx-auto">
              <p className="text-red-600 dark:text-red-400 text-lg">{error}</p>
            </div>
          </div>
        )}
        
        {!loading && !error && (
          challenges.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 auto-rows-fr">
              {challenges.map((challenge) => (
                <ChallengeCard key={challenge.id} challenge={challenge} />
              ))}
            </div>
          ) : (
            <div className="glass-card p-12 text-center max-w-2xl mx-auto">
              <div className="text-6xl mb-4">🎯</div>
              <p className="text-slate-500 dark:text-slate-400 text-xl">
                No challenges available right now. Check back soon!
              </p>
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default Home;

