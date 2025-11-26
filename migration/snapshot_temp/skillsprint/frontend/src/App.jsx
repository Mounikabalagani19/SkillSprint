import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Import components and pages
import Header from "./components/Header.jsx";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";
import Leaderboard from "./pages/Leaderboard.jsx";
import Modules from "./pages/Modules.jsx";
import ModulePython from "./pages/ModulePython.jsx";
import ModuleLevel from "./pages/ModuleLevel.jsx";
import ModuleJava from "./pages/ModuleJava.jsx";
import Dashboard from "./pages/Dashboard.jsx";

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/modules" element={<Modules />} />
            <Route path="/modules/python" element={<ModulePython />} />
            <Route path="/modules/python/:level" element={<ModuleLevel moduleName="python" />} />
            <Route path="/modules/java" element={<ModuleJava />} />
            <Route path="/modules/java/:level" element={<ModuleLevel moduleName="java" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

