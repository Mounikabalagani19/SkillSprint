import React, { useState, useEffect } from 'react';
import { Users, Copy, Wrench } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

const MentorDashboard = () => {
    const { user } = useAuth();
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        alert("Join code copied to clipboard!");
    };

    useEffect(() => {
        const fetchStudents = async () => {
            try {
                const response = await api.getMentorStudents();
                setStudents(response.data);
            } catch (err) {
                console.error("Error fetching students:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchStudents();
    }, []);

    return (
        <div className="container mx-auto px-4 py-12">
            <div className="flex flex-col md:flex-row md:items-center justify-between mb-12 gap-6">
                <h1 className="text-4xl font-bold text-slate-800 dark:text-slate-100 flex items-center">
                    Mentor Dashboard
                </h1>

                {user?.join_code && (
                    <div className="glass-card px-6 py-4 flex items-center justify-between border-l-4 border-l-purple-600 min-w-[300px]">
                        <div>
                            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Your Mentor Join Code</p>
                            <p className="text-2xl font-mono font-bold text-purple-600">{user.join_code}</p>
                        </div>
                        <button
                            onClick={() => copyToClipboard(user.join_code)}
                            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors text-slate-500"
                            title="Copy Code"
                        >
                            <Copy size={20} />
                        </button>
                    </div>
                )}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Students List */}
                <div className="glass-card p-8 lg:col-span-2">
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center">
                            <Users className="text-purple-600 mr-3" size={28} />
                            <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">My Students</h2>
                        </div>
                        <span className="text-sm text-slate-500 bg-slate-100 dark:bg-slate-800 px-3 py-1 rounded-full">
                            {students.length} student{students.length !== 1 ? 's' : ''}
                        </span>
                    </div>
                    {loading ? (
                        <div className="flex items-center justify-center py-12">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                        </div>
                    ) : students.length > 0 ? (
                        <div className="space-y-4">
                            {students.map(student => (
                                <div key={student.id} className="flex justify-between items-center p-4 bg-white/30 dark:bg-slate-800/30 rounded-xl border border-slate-200/50 dark:border-slate-700/50 hover:shadow-md transition-shadow">
                                    <div>
                                        <p className="font-bold text-slate-800 dark:text-slate-100">{student.username}</p>
                                        <p className="text-sm text-slate-500">{student.email}</p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-purple-600 font-bold">{student.xp} XP</p>
                                        <p className="text-sm text-orange-500">🔥 {student.streak} Streak</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <Users className="mx-auto text-slate-300 dark:text-slate-600 mb-4" size={48} />
                            <p className="text-slate-500">No students assigned yet.</p>
                            <p className="text-sm text-slate-400 mt-2">Share your join code to get students!</p>
                        </div>
                    )}
                </div>

                {/* Quick Actions */}
                <div className="space-y-6">
                    <Link to="/mentor/tools" className="glass-card p-6 block group hover:scale-[1.02] transition-transform border-l-4 border-l-blue-600">
                        <div className="flex items-center mb-3">
                            <Wrench className="text-blue-600 mr-3" size={24} />
                            <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100">Mentor Tools</h3>
                        </div>
                        <p className="text-slate-600 dark:text-slate-400 text-sm">Create modules from PDFs and upload challenge tracks.</p>
                        <span className="text-blue-600 text-sm font-medium mt-3 inline-block group-hover:underline">Go to Tools →</span>
                    </Link>

                    <div className="glass-card p-6 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20">
                        <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-3">Quick Stats</h3>
                        <div className="space-y-3">
                            <div className="flex justify-between">
                                <span className="text-slate-600 dark:text-slate-400">Total Students</span>
                                <span className="font-bold text-purple-600">{students.length}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-slate-600 dark:text-slate-400">Avg XP</span>
                                <span className="font-bold text-blue-600">
                                    {students.length > 0 
                                        ? Math.round(students.reduce((sum, s) => sum + s.xp, 0) / students.length)
                                        : 0}
                                </span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-slate-600 dark:text-slate-400">Active Streaks</span>
                                <span className="font-bold text-orange-500">
                                    {students.filter(s => s.streak > 0).length}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MentorDashboard;
