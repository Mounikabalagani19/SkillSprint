import React from "react";
import { Link } from "react-router-dom";

export default function ModuleJava() {
  const levels = [
    { key: "beginner", title: "Beginner", desc: "Start here to warm up your Java fundamentals." },
    { key: "intermediate", title: "Intermediate", desc: "Level up with practical Java problem-solving." },
    { key: "expert", title: "Expert", desc: "Challenge yourself with advanced Java scenarios." },
  ];

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-slate-800 dark:text-slate-100">Java Module</h1>
        <p className="text-slate-600 dark:text-slate-300 mt-3 max-w-2xl mx-auto">
          Select your difficulty. You’ll see one question at a time and can progress sequentially.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {levels.map((lvl) => (
          <div key={lvl.key} className="module-card flex flex-col">
            <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">{lvl.title}</h2>
            <p className="text-slate-600 dark:text-slate-300 mt-2 flex-grow">{lvl.desc}</p>
            <Link to={`/modules/java/${lvl.key}`} className="btn-primary mt-6">Start</Link>
          </div>
        ))}
      </div>
    </div>
  );
}
