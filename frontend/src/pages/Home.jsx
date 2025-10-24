import React, { useState, useEffect } from "react";
import api from "../services/api";
import ChallengeCard from "../components/ChallengeCard.jsx";
import { Link } from "react-router-dom";

const Home = () => {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [favourites, setFavourites] = useState([]);

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        setLoading(true);
        const response = await api.getChallenges();
        // Debug: log what the API returns to help diagnose missing cards
        console.log("/challenges response:", {
          count: Array.isArray(response.data) ? response.data.length : 'n/a',
          sample: Array.isArray(response.data) && response.data.length ? response.data[0] : response.data,
        });
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

  useEffect(() => {
    try {
      const raw = localStorage.getItem('favouriteModules');
      setFavourites(raw ? JSON.parse(raw) : []);
    } catch (e) {
      setFavourites([]);
    }
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
          challenges && challenges.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 auto-rows-fr">
              {challenges.map((challenge) => (
                <ChallengeCard key={challenge.id} challenge={challenge} />
              ))}
            </div>
          ) : (
            <div className="glass-card p-12 text-center max-w-2xl mx-auto">
              <div className="text-6xl mb-4">🎯</div>
              <p className="text-slate-500 dark:text-slate-400 text-xl">
                No challenges available right now. If you just deployed or switched databases,
                please refresh in a moment while the server seeds data.
              </p>
              <p className="mt-3 text-slate-400 text-sm">
                Tip: Make sure you’re logged in to submit answers. Logged-out users see Day 1.
              </p>
            </div>
          )
        )}

        {/* Modules quick access section */}
        <div className="mt-16">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl md:text-3xl font-bold text-slate-700 dark:text-slate-200">Practice Modules</h3>
            <Link to="/modules" className="btn-secondary">View all</Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {favourites && favourites.length > 0 ? (
              favourites.map((slug) => {
                const modulesMap = {
                  python: { title: 'Python', href: '/modules/python', desc: 'Choose Beginner, Intermediate, or Expert and practice sequentially.' },
                  java: { title: 'Java', href: '/modules/java', desc: 'Choose Beginner, Intermediate, or Expert and practice sequentially.' }
                };
                const m = modulesMap[slug];
                if (!m) return null;
                return (
                  <Link key={slug} to={m.href} className="module-card block relative">
                        <div className="absolute right-4 top-4 w-9 h-9 inline-flex items-center justify-center rounded-full shadow-sm border text-rose-500 bg-rose-50/30 border-rose-100/30">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4" style={{ transform: 'translate(-0.5px, -1px)' }}>
                            <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L12 8.343l3.172-3.171a4 4 0 115.656 5.656L12 21.657 3.172 10.828a4 4 0 010-5.656z" clipRule="evenodd" />
                          </svg>
                        </div>
                    <div className="text-sm text-slate-500 dark:text-slate-400">Module</div>
                    <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">{m.title}</div>
                    <p className="mt-2 text-slate-600 dark:text-slate-300">{m.desc}</p>
                  </Link>
                );
              })
            ) : (
              <div className="glass-card p-6 text-center max-w-2xl mx-auto">
                <p className="text-slate-600 dark:text-slate-300">You have no favourite modules yet. Go to <a href="/modules" className="underline">Modules</a> to mark your favourites using the heat icon.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

