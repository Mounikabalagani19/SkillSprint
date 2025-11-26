import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../services/api";

export default function ModuleLevel({ moduleName = 'python' }) {
  const { level } = useParams();
  const [items, setItems] = useState([]);
  const [status, setStatus] = useState({ loading: true, error: null });
  const [idx, setIdx] = useState(0); // current question index
  const [input, setInput] = useState("");
  const [message, setMessage] = useState("");
  const [wasCorrect, setWasCorrect] = useState(null); // true/false/null
  const current = items[idx] ?? null;
  const total = items.length;

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        setStatus({ loading: true, error: null });
        setIdx(0);
        setInput("");
        setMessage("");
  const res = await api.getModuleItems(level, moduleName);
        if (!active) return;
        setItems(res.data || []);
        setStatus({ loading: false, error: null });
      } catch (e) {
        console.error("load module items", e);
        if (!active) return;
        setStatus({ loading: false, error: "Failed to load module items. Are you logged in?" });
      }
    }
    load();
    return () => { active = false; };
  }, [level]);

  const onSubmit = async () => {
    if (!current) return;
    try {
  const res = await api.submitModuleAnswer(level, { id: current.id, answer: input }, moduleName);
      const ok = !!res?.data?.success;
      setWasCorrect(ok);
      setMessage(res?.data?.message || (ok ? "Correct" : "Incorrect"));
    } catch (e) {
      const msg = e?.response?.data?.detail || e?.response?.data?.message || "Submission failed";
      setWasCorrect(false);
      setMessage(msg);
    }
  };

  const next = () => {
    setIdx((n) => Math.min(n + 1, Math.max(0, items.length - 1)));
    setInput("");
  setMessage("");
  setWasCorrect(null);
  };

  const prev = () => {
    setIdx((n) => Math.max(0, n - 1));
    setInput("");
  setMessage("");
  setWasCorrect(null);
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex items-center justify-between mb-6">
  <h1 className="text-3xl md:text-4xl font-extrabold text-slate-800 dark:text-slate-100 capitalize">{moduleName === 'java' ? 'Java' : 'Python'} · {level}</h1>
  <Link to={moduleName === 'java' ? "/modules/java" : "/modules/python"} className="btn-secondary">Change level</Link>
      </div>

      {/* Carousel of questions */}
      {!status.loading && !status.error && total > 0 && (
        <div className="max-w-3xl mx-auto mb-6 flex flex-wrap gap-2 justify-center">
          {items.map((q, i) => {
            const isActive = i === idx;
            const isDone = !!q.completed;
            return (
              <button
                key={q.id}
                onClick={() => { setIdx(i); setInput(""); setMessage(""); setWasCorrect(null); }}
                className={`px-3 py-1 rounded-full text-sm transition-all duration-300 focus:outline-none 
                  ${isActive ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg scale-105' : 'bg-white/70 dark:bg-slate-800/70 text-slate-700 dark:text-slate-200 border border-slate-200/50 dark:border-slate-700/50 hover:scale-105'}
                  ${isDone ? 'ring-2 ring-green-400/70 dark:ring-green-500/50' : 'ring-0'}`}
                title={isDone ? 'Completed' : 'Not completed'}
              >
                {i + 1}
              </button>
            );
          })}
        </div>
      )}

      {status.loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-purple-600"></div>
          <p className="text-slate-500 dark:text-slate-400 mt-3">Loading…</p>
        </div>
      )}

      {status.error && (
        <div className="glass-card p-4 max-w-xl mx-auto text-center text-red-600 dark:text-red-400">{status.error}</div>
      )}

      {!status.loading && !status.error && current && (
        <div className="max-w-2xl mx-auto module-card">
          <div className="text-sm text-slate-500 dark:text-slate-400">Question {idx + 1} of {items.length}</div>
          <div className="mt-1 text-xs text-slate-500 dark:text-slate-400">Level: {current.level}</div>

          <div className="mt-3 text-lg text-slate-800 dark:text-slate-100">
            {current.question || `Provide the correct answer for item #${current.id}.`}
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">Your Answer</label>
            <input
              type="text"
              className="mt-1 w-full rounded-md border border-slate-300 dark:border-slate-600 bg-white/70 dark:bg-slate-800/70 p-2 focus:outline-none focus:ring-2 focus:ring-purple-600"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your answer"
            />
            <button className={`btn-primary mt-3`} onClick={onSubmit}>Submit</button>
            {message && (
              <div className={`mt-2 text-sm ${wasCorrect === true ? 'text-green-600 dark:text-green-400' : wasCorrect === false ? 'text-red-600 dark:text-red-400' : 'text-slate-700 dark:text-slate-200'}`}>
                {message}
              </div>
            )}
          </div>

          {current.explanation && (
            <details className="mt-4">
              <summary className="cursor-pointer text-slate-600 dark:text-slate-300">Show explanation</summary>
              <div className="mt-2 text-slate-700 dark:text-slate-200">
                {/* Answer string is intentionally not included in GET response to prevent peeking. */}
                <div className="mt-1">{current.explanation}</div>
              </div>
            </details>
          )}

          <div className="mt-6 flex items-center justify-between">
            <button className="btn-secondary" onClick={prev} disabled={idx === 0}>Previous</button>
            {idx < items.length - 1 ? (
              <button className="btn-primary" onClick={next}>Next</button>
            ) : (
              <Link to={moduleName === 'java' ? '/modules/java' : '/modules/python'} className="btn-primary">Finish</Link>
            )}
          </div>
        </div>
      )}

      {!status.loading && !status.error && !current && (
        <div className="glass-card p-6 text-center max-w-xl mx-auto">
          <div className="text-lg">No items found.</div>
          <Link to="/modules/python" className="btn-primary mt-4 inline-block">Back to levels</Link>
        </div>
      )}
    </div>
  );
}
